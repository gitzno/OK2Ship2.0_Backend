#!/bin/bash

# Lệnh này giúp script tự động in ra màn hình các biến bị rỗng/chưa khai báo
set -u

# 1. Khởi động SQL Server ở chế độ background
/opt/mssql/bin/sqlservr &
pid=$!

echo "Đang chờ SQL Server khởi động..."

# 2. Vòng lặp kiểm tra trạng thái SQL Server
for i in {1..60}; do
    echo "========================================="
    echo "Đang thử kết nối lần $i..."
    
    # ĐÃ SỬA: Đổi localhost thành 127.0.0.1 và XÓA > /dev/null 2>&1
    # Bất kỳ lỗi nào của sqlcmd (sai pass, thiếu port, từ chối kết nối) sẽ in thẳng ra log
    /opt/mssql-tools18/bin/sqlcmd -S 127.0.0.1 -U sa -P "$MSSQL_SA_PASSWORD" -C -Q "SELECT 1"
    
    # Lưu lại mã lỗi (exit code) của lệnh sqlcmd vừa chạy
    SQLCMD_EXIT_CODE=$?
    
    if [ $SQLCMD_EXIT_CODE -eq 0 ]; then
        echo "✅ KẾT NỐI THÀNH CÔNG! SQL Server đã sẵn sàng sau $i lần thử!"
        echo "========================================="
        
        # 3. Thực thi tự động toàn bộ file .sql
        echo "Bắt đầu hợp nhất và thực thi toàn bộ script trong thư mục scripts..."
        
        # Sửa localhost thành 127.0.0.1 ở bước thực thi script luôn
        cat /usr/src/app/scripts/*.sql | /opt/mssql-tools18/bin/sqlcmd -S 127.0.0.1 -U sa -P "$MSSQL_SA_PASSWORD" -C
        
        if [ $? -eq 0 ]; then
            echo "🎉 Khởi tạo toàn bộ Database, Partition và Tables hoàn tất thành công!"
        else
            echo "❌ LỖI: Có lỗi xảy ra trong quá trình thực thi các file SQL."
        fi
        
        break
    else
        echo "⚠️ KẾT NỐI THẤT BẠI. Mã lỗi (Exit Code): $SQLCMD_EXIT_CODE"
        echo "Tiếp tục chờ..."
    fi
    
    sleep 2
done

# 4. Giữ container luôn chạy
echo "Hệ thống đang vận hành..."
wait $pid