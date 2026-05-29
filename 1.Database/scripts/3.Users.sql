-- 3.Users.sql
USE [OK2SHIP_SMT];

create table dbo.Users(
	-- Internal ID
	UserIDI INT IDENTITY(1,1) NOT NULL ,

	UserID UNIQUEIDENTIFIER default  NEWID() NOT NULL,
	
	Username VARCHAR(50) NOT NULL,

	EmployeeID VARCHAR(50) NOT NULL,
	
	PasswordHash VARCHAR(255) NOT NULL,
	
	-- User status
	-- 1 Active, 2 Pending, 3 Suspended, 4 Deleted
	UserStatus TINYINT default 1 NOT NULL,


	-- Security & Account Lockout (Chống Brute Force)
    FailedLoginAttempts INT DEFAULT 0 NOT NULL,
	CreatedDateTimeUTC DATETIME2(7) DEFAULT SYSUTCDATETIME() NOT NULL,
    LastModifiedDateTimeUTC DATETIME2(7) DEFAULT SYSUTCDATETIME() NOT NULL,
    LastLoginDateTimeUTC DATETIME2(7) NULL,
    LastLoginIpAddress VARCHAR(45) NULL,

	CONSTRAINT PK_Users_UserIDI PRIMARY KEY CLUSTERED (UserIDI),
    CONSTRAINT UQ_Users_UserID UNIQUE NONCLUSTERED (UserID),
    CONSTRAINT UQ_Users_EmployeeID UNIQUE NONCLUSTERED (EmployeeID),
    CONSTRAINT UQ_Users_Username UNIQUE NONCLUSTERED (Username)
);
GO

-- 2. Tạo Trigger tự động cập nhật ngày chỉnh sửa cuối cùng (Automated Audit)
CREATE TRIGGER dbo.TR_Users_UpdateLastModified
ON dbo.Users
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE dbo.Users
    SET LastModifiedDateTimeUTC = SYSUTCDATETIME()
    FROM dbo.Users u
    INNER JOIN inserted i ON u.UserId = i.UserId;
END;
GO


