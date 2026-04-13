-- 1. Tạo bảng
CREATE TABLE [dbo].[PEEL_TEST_NAS](
    [ID] [INT] IDENTITY(1,1) NOT NULL,
    [ItemCode] [VARCHAR](50) NOT NULL, 
    [LotNo] [VARCHAR](50) NOT NULL,
    [Type] [VARCHAR](20) NOT NULL,
    [Data] [NVARCHAR](MAX) NULL,             
    [LocationImg] [NVARCHAR](500) NULL,      
    [CreatedDate] [DATETIME] NOT NULL 
        CONSTRAINT [DF_PEEL_TEST_NAS_CreatedDate] DEFAULT (GETDATE()),

    CONSTRAINT [PK_PEEL_TEST_NAS] PRIMARY KEY CLUSTERED ([ID] ASC, [CreatedDate] ASC)
) ON [PS_Quarterly]([CreatedDate])
WITH (DATA_COMPRESSION = PAGE); -- Nén bảng chính
GO

-- 2. Tạo Index "Siêu nhẹ" (Không INCLUDE Data để tiết kiệm ổ cứng)
CREATE NONCLUSTERED INDEX [IX_PEEL_TEST_NAS_Search] 
ON [dbo].[PEEL_TEST_NAS] ([ItemCode], [LotNo], [Type])
ON [PS_Quarterly]([CreatedDate])
WITH (DATA_COMPRESSION = PAGE); -- Nén mục lục
GO