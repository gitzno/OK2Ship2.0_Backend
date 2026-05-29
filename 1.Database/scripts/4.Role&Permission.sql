USE [OK2SHIP_SMT]

CREATE TABLE dbo.Roles(
	RoleID INT IDENTITY(1,1) PRIMARY KEY
	RoleName VARCHAR(50) NOT NULL UNIQUE,
	Description NVARCHAR(255) NULL

)

CREATE TABLE dbo.Permissions(
	PermissionID INT IDENTITY(1,1) PRIMARY KEY,
	PermissionCode VARCHAR(100) NOT NULL UNIQUE,
	Description NVARCHAR(255) NULL
)

CREATE TABLE dbo.UserRoles(
	UserIDI INT NOT NULL,
	RoleID INT NOT NULL,
	CONSTRAINT PK_UserRoles PRIMARY KEY CLUSTERED (UserIDI, RoleID),
	CONSTRAINT FK_UserRoles_Users FOREIGN KEY (UserIDI) REFERENCES dbo.Users(UserIDI) ON DELETE CASCADE,
	CONSTRAINT FK_UserRoles_RoleID FOREIGN KEY (RoleID) REFERENCES dbo.Roles(RoleID) ON DELETE CASCADE
)

CREATE TABLE dbo.RolePermissions(
	RoleID INT NOT NULL,
	PermissionID INT NOT NULL,
	CONSTRAINT PK_RolePermissions PRIMARY KEY CLUSTERED (RoleId, PermissionId),
    CONSTRAINT FK_RolePermissions_Roles FOREIGN KEY (RoleId) REFERENCES dbo.Roles(RoleId) ON DELETE CASCADE,
    CONSTRAINT FK_RolePermissions_Permissions FOREIGN KEY (PermissionId) REFERENCES dbo.Permissions(PermissionId) ON DELETE CASCADE
);
/*
INSERT INTO dbo.Permissions (PermissionCode, Description) VALUES 
('amind:create', N'Quyền tạo mới vận đơn'),
('shipment:approve', N'Quyền phê duyệt xuất hàng (OK2Ship)'),
('shipment:view', N'Quyền xem danh sách vận đơn');

-- Nạp vai trò
INSERT INTO dbo.Roles (RoleName, Description) VALUES 
('ADMIN', N'Trưởng chuyền - Có quyền duyệt hàng'),
('OPERATOR', N'Công nhân vận hành - Chỉ được tạo và xem đơn');

-- Gán quyền cho vai trò (Giả định ID tự tăng từ 1)
-- LINE_LEADER có tất cả quyền
INSERT INTO dbo.RolePermissions (RoleId, PermissionId) VALUES (1, 1), (1, 2), (1, 3);
-- OPERATOR chỉ có quyền tạo và xem, không có quyền duyệt (Id 2)
INSERT INTO dbo.RolePermissions (RoleId, PermissionId) VALUES (2, 1), (2, 3);
*/
