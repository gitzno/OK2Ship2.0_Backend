USE [OK2SHIP_SMT]
GO

-- ==========================================
-- 1. BẢNG ROLES (VAI TRÒ)
-- ==========================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Roles' and xtype='U')
BEGIN
    CREATE TABLE dbo.Roles(
        RoleID INT IDENTITY(1,1) PRIMARY KEY,
        RoleName VARCHAR(50) NOT NULL UNIQUE,
        Description NVARCHAR(255) NULL
    )
    PRINT 'Da tao bang Roles.'
END
GO

-- ==========================================
-- 2. BẢNG PERMISSIONS (QUYỀN HẠN)
-- ==========================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Permissions' and xtype='U')
BEGIN
    CREATE TABLE dbo.Permissions(
        PermissionID INT IDENTITY(1,1) PRIMARY KEY,
        PermissionCode VARCHAR(100) NOT NULL UNIQUE,
        Description NVARCHAR(255) NULL
    )
    PRINT 'Da tao bang Permissions.'
END
GO

-- ==========================================
-- 3. BẢNG USER_ROLES (GÁN VAI TRÒ CHO USER)
-- ==========================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='UserRoles' and xtype='U')
BEGIN
    CREATE TABLE dbo.UserRoles(
        UserIDI INT NOT NULL, 
        RoleID INT NOT NULL,
        
        CONSTRAINT PK_UserRoles PRIMARY KEY CLUSTERED (UserIDI, RoleID),
        CONSTRAINT FK_UserRoles_Users FOREIGN KEY (UserIDI) REFERENCES dbo.Users(UserIDI) ON DELETE CASCADE,
        CONSTRAINT FK_UserRoles_Roles FOREIGN KEY (RoleID) REFERENCES dbo.Roles(RoleID) ON DELETE CASCADE
    )
    PRINT 'Da tao bang UserRoles.'
END
GO

-- ==========================================
-- 4. BẢNG ROLE_PERMISSIONS (GÁN QUYỀN CHO VAI TRÒ)
-- ==========================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='RolePermissions' and xtype='U')
BEGIN
    CREATE TABLE dbo.RolePermissions(
        RoleID INT NOT NULL,
        PermissionID INT NOT NULL,
        
        CONSTRAINT PK_RolePermissions PRIMARY KEY CLUSTERED (RoleID, PermissionID),
        CONSTRAINT FK_RolePermissions_Roles FOREIGN KEY (RoleID) REFERENCES dbo.Roles(RoleID) ON DELETE CASCADE,
        CONSTRAINT FK_RolePermissions_Permissions FOREIGN KEY (PermissionID) REFERENCES dbo.Permissions(PermissionID) ON DELETE CASCADE
    )
    PRINT 'Da tao bang RolePermissions.'
END
GO

-- ==========================================
-- 5. NẠP DỮ LIỆU MẪU (SEED DATA)
-- ==========================================

-- Nạp Role (Bỏ cột RoleID ra để SQL tự động sinh số 1)
IF NOT EXISTS (SELECT 1 FROM dbo.Roles WHERE RoleName = 'ADMIN')
BEGIN
    INSERT INTO dbo.Roles (RoleName, Description) 
    VALUES ('ADMIN', N'Quản trị viên hệ thống - Toàn quyền');
    PRINT 'Da nap Role ADMIN.'
END
GO

-- Nạp Permissions (Bỏ PermissionID ra để SQL tự động sinh số 1, 2, 3)
IF NOT EXISTS (SELECT 1 FROM dbo.Permissions WHERE PermissionCode = 'admin:create')
BEGIN
    INSERT INTO dbo.Permissions (PermissionCode, Description) VALUES 
    ('admin:create', N'Quyền tạo người dùng'),
    ('admin:approve', N'Quyền chỉnh sửa người dùng'),
    ('admin:view', N'Quyền xem danh sách người dùng');
    PRINT 'Da nap cac Permissions.'
END
GO

-- Nạp RolePermissions (Giả định ADMIN là Role 1, và 3 quyền trên là 1, 2, 3)
IF NOT EXISTS (SELECT 1 FROM dbo.RolePermissions WHERE RoleID = 1 AND PermissionID = 1)
BEGIN
    INSERT INTO dbo.RolePermissions (RoleID, PermissionID) 
    VALUES (1, 1), (1, 2), (1, 3);
    PRINT 'Da gan quyen cho Role ADMIN.'
END
GO