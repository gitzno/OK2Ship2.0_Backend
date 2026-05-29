# Week 4:
## Worker_UI
UI worker là phần mềm cho công nhân có thể truy cập thao tác với dữ liệu. Để việc đọc file excel có hiệu suất cao nên chỉ sử dụng epplus x asp.net. Vậy nên có hai phương án:

- <b>Phương án đọc ở client</b>: Sử dụng giao diện của .net để đọc (winform, wpf, blazor...) rồi chỉ lưu dữ liệu thô
Ưu điểm: Giảm tải cho server
Nhược điểm: Giao diện khó có thể tối ưu, thay đổi đồng thời gây khó khăn.

- <b>Phương án đọc ở server</b>: Sử dụng API và SDKS3 để upload dữ liệu lên máy chủ rồi xử lý bằng service asp.net. Rồi đọc trong máy chủ.
Ưu điểm: Giao diện đẹp đa nền tảng. Logic cốt lõi tập chung ở server.
Nhược điểm: Server làm nhiều việc.

Tạm thời tôi sẽ sử dụng sẽ triển khai bằng phương án đọc ở server. Với logic upload sử dụng sdk S3 và sử dụng server Upload API.


# Week 3:
## Database
Ưu điểm của kiến trúc chia mảnh của tôi
```
Action              | Normal                      | Kiến trúc mới
--------------------------------------------------------------------------
Tìm kiếm DATA mới   | Quét toàn bộ dữ liệu        | Tìm quý gần nhất
--------------------------------------------------------------------------
Dung lượng lưu trữ  | 100% Dung lượng thực tế     | Giảm ~60%
--------------------------------------------------------------------------
Tìm kiếm DATA cũ    | Quét toàn bộ dữ liệu        | Ổn định(Olog(n))
--------------------------------------------------------------------------
Xóa dữ liệu hết hạn | tìm kiếm và xóa             | tức thì (O(1))
--------------------------------------------------------------------------
```

## Object storage & API Upload service
Tôi đã phải chuyển từ MINIO sang SeaweedFS do lo ngại vấn đề pháp lý nếu phần mềm này được triển khai.
Minio đã chuyển giấy phép.

- Triển khai việc lưu trữ ví nóng => ví lạnh => Hết hạn
- Triển khai API Upload version 1 with  asp.net .net10

Lỗi khi config S3 for object storage ?
Chuyển lại sang sử dụng MINIO trong phần mềm sẽ sử dụng S3 sdk để giao tiếp sau cắm vào 1 storage object khác sau.

### Triển khai việc lưu trữ ví nóng => ví lạnh => Hết hạn
Khởi tạo 2 minio:
<br> Minio HOT STORAGE: 
- Triển khai trên 4 vùng ổ cứng => Lấy hiệu năng đọc ghi cũng như Distributed
- Mở trên cổng 9000 (API) và 9001 (Console)
- Lưu trữ trong vòng 1 quý (4 tháng) cho cả image và report
```
#docker-compose
# --- CỤM 1: HOT STORAGE (SSD) ---
  minio-hot:
    image: minio/minio:latest
    container_name: minio_hot_ssd
    ports:
      - "9000:9000"   # API
      - "9001:9001"   # Console
    volumes:
      - ${FOLDER_PATH_SSD}/data1:/data1
      - ${FOLDER_PATH_SSD}/data2:/data2
      - ${FOLDER_PATH_SSD}/data3:/data3
      - ${FOLDER_PATH_SSD}/data4:/data4
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER_HOT}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD_HOT}
    command: server /data1 /data2 /data3 /data4 --console-address ":9001"
    restart: always
```
<br> Minio COLD STORAGE: 
- Triển khai trên 1 vùng ổ cứng
- Mở trên cổng 9002 (API) và 9003 (Console)
- Thời gian lưu trữ = thời gian còn lại - 120days (4 month) cho cả image và report
```
# --- CỤM 2: COLD STORAGE (HDD) ---
  minio-cold:
    image: minio/minio:latest
    container_name: minio_cold_hdd
    ports:
      - "9002:9000"   # API (Đổi sang 9002 để tránh trùng)
      - "9003:9001"   # Console (Đổi sang 9003)
    volumes:
      - ${FOLDER_PATH_NAS}/data:/data
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER_COLD}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD_COLD}
    command: server /data --console-address ":9001"
    restart: always
```
### Triển khai API Upload x S3
Đầu tiên để đơn giản nhanh chóng tôi sẽ triển khai với ASP.net
- Tôi sử dụng kiến trúc clean architechture quen thuộc và .net 10
- Khởi tạo repository lữu trữ giao tiếp s3 với các giao tiếp đó 
- Sử dụng cấu hình nhiều ví để có thể thao tác với nhiều ví cùng 1 lúc thông qua cùng 1 giao thức:
```
var storageSettings = builder.Configuration.GetSection("StorageSettings");
var provider = storageSettings["MinIO"];
// cấu hình ví nóng
var hotS3Config = new AmazonS3Config
{
    ServiceURL = storageSettings["HotEndpoint"], 
    ForcePathStyle = true
};

builder.Services.AddKeyedSingleton<IAmazonS3>("HotStorage", new AmazonS3Client(storageSettings["HotAccessKey"], storageSettings["HotSecretKey"], hotS3Config));


builder.Services.AddScoped<IStorageRepository, StorageObjectRepository>();
```
- Dựa vào thư viện [Amazon.S3](https://docs.aws.amazon.com/sdk-for-net/v3/developer-guide/csharp_s3_code_examples.html) viết các hàm giao tiếp với dịch vụ lưu trữ
- Có điều kiện khởi tạo lưu trữ phân tán và lưu trữ cục bộ bằng nas chung qua giáo tiếp S3
- Làm một dịch vụ khởi tạo khi Upload_API chạy sẽ kiểm tra xem cấu trúc bucket có tồn tại không (2 bucket cho report và image)

Tiếp theo tôi sẽ làm 1 api upload folder logfile lên hệ thống

# Week 2:
## Database
Như tuần trước tôi sẽ làm lần lượt hệ thông database của tôi, ở đây tôi khởi tạo tự động bằng DOCKER và code T-SQL:
 - tạo docker file cho pull mssql về và chạy entrypoint để tự động chạy các scrpit trong folder ./script 
 - đẩy docker file vào trong docker-compose thêm biến ${MSSQL_PASSWORD} vào trong env
 => docker compose tự động khởi tạo

0.Init_DB.sql: Tạo database OK2SHIP_SMT 2.0 
```
USE [master]
GO
/****** Object:  Database [OK2SHIP_SMT]    Script Date: 3/20/2026 5:31:44 PM ******/
CREATE DATABASE [OK2SHIP_SMT]

```

1.init_partition: 
 - Tạo Partition Function (PF_Quarterly): Cắm các mốc thời gian chia theo từng quý (2024, 2025, 2026...). Đây là "Luật chia".

- Tạo Partition Scheme (PS_Quarterly): Gắn luật chia này lên ổ cứng. Đây là "Bản đồ lưu trữ". 
```
USE [OK2SHIP_SMT];
GO

-- =========================================================
-- GIAI ĐOẠN 1: TẠO LUẬT CHIA (FUNCTION) VÀ BẢN ĐỒ (SCHEME)
-- =========================================================

-- 2. Tạo Partition Function: Chia theo từng Quý
-- Tôi đã tạo sẵn các mốc từ năm 2024 đến hết 2026 cho bạn.
CREATE PARTITION FUNCTION PF_Quarterly (DATETIME)
AS RANGE RIGHT FOR VALUES (
    '2024-01-01', '2024-04-01', '2024-07-01', '2024-10-01',
    '2025-01-01', '2025-04-01', '2025-07-01', '2025-10-01',
    '2026-01-01', '2026-04-01', '2026-07-01', '2026-10-01'
);
GO

-- 3. Tạo Partition Scheme: Gắn Luật chia trên vào ổ đĩa PRIMARY
CREATE PARTITION SCHEME PS_Quarterly
AS PARTITION PF_Quarterly
ALL TO ([PRIMARY]);
GO
```


2. Tạo ra funciton truy vấn đỉnh cao
```
USE [OK2SHIP_SMT];
GO

CREATE PROCEDURE [dbo].[sp_UniversalSearch]
    @TableName NVARCHAR(128),  -- Tham số nhận tên bảng (ví dụ: 'PEEL_TEST_NAS', 'ACF_BONDING_NAS')
    @ItemCode VARCHAR(20),
    @LotNo VARCHAR(20),
    @Type VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;

    -- 1. BẢO MẬT: Kiểm tra xem bảng có tồn tại không (Chống SQL Injection)
    IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = @TableName)
    BEGIN
        RAISERROR('Tên bảng không tồn tại trong hệ thống!', 16, 1);
        RETURN;
    END

    -- Hàm QUOTENAME sẽ tự động bọc tên bảng thành dạng [TenBang] cho chuẩn cú pháp
    DECLARE @SafeTableName NVARCHAR(256) = QUOTENAME(@TableName);
    DECLARE @DynamicSQL NVARCHAR(MAX);

    -- 2. "LẮP RÁP" câu lệnh SQL Thác đổ
    SET @DynamicSQL = N'
        -- Bước 1: Ưu tiên tìm 3 tháng gần nhất (Quét ít Partition)
        SELECT * INTO #TempResult 
        FROM dbo.' + @SafeTableName + N'
        WHERE ItemCode = @p_ItemCode AND LotNo = @p_LotNo AND Type = @p_Type
          AND CreatedDate >= DATEADD(MONTH, -3, GETDATE());

        -- Kiểm tra nếu có dữ liệu ở Bước 1
        IF EXISTS (SELECT 1 FROM #TempResult)
        BEGIN
            -- Trả về luôn cho lẹ
            SELECT * FROM #TempResult;
        END
        ELSE
        BEGIN
            -- Bước 2: Không thấy thì mới tìm full toàn bộ lịch sử (Dự phòng)
            SELECT * FROM dbo.' + @SafeTableName + N'
            WHERE ItemCode = @p_ItemCode AND LotNo = @p_LotNo AND Type = @p_Type;
        END
    ';

    -- 3. THỰC THI câu lệnh SQL Động một cách an toàn
    EXEC sp_executesql 
        @stmt = @DynamicSQL,
        @params = N'@p_ItemCode VARCHAR(20), @p_LotNo VARCHAR(20), @p_Type VARCHAR(20)',
        @p_ItemCode = @ItemCode,
        @p_LotNo = @LotNo,
        @p_Type = @Type;

END;
GO

```


3.x Tạo ra các bảng dữ liệu:
Theo cấu trúc bắt buộc phải có:
[ ] Có cột CreatedDate kiểu DATETIME chưa?

[ ] Khóa chính đã có cả ID và CreatedDate chưa?

[ ] Cuối lệnh CREATE TABLE đã có ON PS_Quarterly(CreatedDate) chưa?

[ ] Các cột tìm kiếm đã được gom vào Covering Index chưa?

[ ] Tên các cột lõi có khớp với Stored Procedure vạn năng không?

Form tạo bảng truy vấn nhanh:

```
-- 1. Tên bảng: Thay thế [PEEL_TEST_NAS] bằng tên bảng mới của bạn
CREATE TABLE [dbo].[PEEL_TEST_NAS](
    [ID] [INT] IDENTITY(1,1) NOT NULL,
    
    -- Các cột định danh (Phải khớp tên để Stored Procedure chạy được)
    [ItemCode] [VARCHAR](50) NOT NULL, 
    [LotNo] [VARCHAR](50) NOT NULL,
    [Type] [VARCHAR](20) NOT NULL,
    
    -- Các cột dữ liệu nặng
    [Data] [NVARCHAR](MAX) NULL,             -- Lưu chuỗi JSON kết quả test
    [LocationImg] [NVARCHAR](500) NULL,      -- Lưu đường dẫn ảnh trên MinIO/Server
    
    -- Cột mốc thời gian (Bắt buộc để phân mảnh)
    [CreatedDate] [DATETIME] NOT NULL 
        CONSTRAINT [DF_TableName_CreatedDate] DEFAULT (GETDATE()),

    -- KHÓA CHÍNH: Bắt buộc chứa CreatedDate để phân mảnh
    CONSTRAINT [PK_PEEL_TEST_NAS] PRIMARY KEY CLUSTERED 
    (
        [ID] ASC, 
        [CreatedDate] ASC
    )
) ON [PS_Quarterly]([CreatedDate]); -- Gắn bảng vào Scheme
GO

-- 2. Tên Index: Thay [IX_PEEL_TEST_Search] cho phù hợp với tên bảng
-- Tạo mục lục siêu tốc chứa sẵn dữ liệu nặng (Covering Index)
CREATE NONCLUSTERED INDEX [IX_PEEL_TEST_Search] 
ON [dbo].[PEEL_TEST_NAS] ([ItemCode], [LotNo], [Type])
ON [PS_Quarterly]([CreatedDate]);
GO
```
# Week 1:

## Background

Tập chung vào logic cốt lõi của dự án xuất dữ liệu

Dự án này để chuyển đổi dự án cũ OK2Ship sang một hệ thống mới trước đây chỉ tập chung vào giải quyết vấn đề trước mắt là:

> UI cho công nhân sử dụng => lưu database => xuất file.

> Gói gọn trong một **project winform**.

Nhưng khi dữ liệu ngày càng nhiều và phức tạp thì phần mềm đã giảm hiệu suất cũng như bảo trì gặp nhiều cản trở khó khăn.

=> Vì vậy tôi quyết định chuyển đổi nó thành hệ thống hướng sự kiện thế hệ mới.

> Trong quá trình sử dụng tôi sẽ vừa làm tài liệu lên kiến trúc và phương pháp chuyển đổi sang cho có thể chuyển đổi nhẹ nhàng sang hệ thống mới.

## Database

Database ban đầu được sử dụng hoàn toàn bằng mssql - lưu ảnh - lưu dữ liệu từng cột VD:

```
//Old table ACF_BONDING
CREATE TABLE [dbo].[ACF_BONDING](
  [ID] [int] NOT NULL,
  [ItemCode] [nvarchar](max) NULL,
  [LotNo] [nvarchar](max) NULL,
  [Pcs_No] [nvarchar](max) NULL,
  [Image_Before] [varbinary](max) NULL,
  [Image_After] [varbinary](max) NULL,
  [Graph] [varbinary](max) NULL,
  [Data] [nvarchar](max) NULL,
  [Operator] [nvarchar](max) NULL,
  [Time_Update] [nvarchar](max) NULL,
  [Remark] [nvarchar](max) NULL
)
```

Hiện có 3 vấn đề lớn ở trong bảng dữ liệu này:

- Dữ liệu có kèm dữ liệu phức tạp
- Dữ liệu trên thực tế chỉ truy vấn đến ItemCode và LotNo
- Chưa đánh index dữ liệu



Hệ quả dẫn tới hệ thống bị treo và không sử dụng được. Dựa vào các vấn đề gặp phải tôi sử dụng kiến trúc cơ sở dữ liệu mới như sau:

- Chuyển đổi từ lưu trữ byte[] Database => object storage.
- Chuyển đổi từ lưu 1 dữ liệu cho 1 itemcode lotno nhiều dòng => 1 dòng
- Đánh Index cho những cột thường truy vấn.
- Sử dụng kỹ thuật patition table để phân mảnh phục vụ việc dữ liệu hết hạn và xóa



## Bước đầu Tập chung vào logic cốt lõi của dự án xuất dữ liệu

Tôi chọn golang là ngôn ngữ đảm nhiệm logic phần này.

### Tại sao là GO / GOLANG

- Tại tôi thích

### Thiết lập cấu trúc thư mục theo chuẩn [Standard Go Project Layout](https://github.com/golang-standards/project-layout/blob/master/README_vi.md)

- Tạo Folder 1.ExportModule
  mkdir cmd\api, cmd\worker, internal\shipment, internal\export, internal\config, pkg\logger, pkg\database, api, deployments
  go mod init ok2ship2.0_export_module

###
