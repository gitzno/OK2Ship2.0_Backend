from typing import Optional
import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, String, Table, Unicode, Uuid, text
from sqlalchemy.dialects.mssql import DATETIME2, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class PEELTESTNAS(Base):
    __tablename__ = 'PEEL_TEST_NAS'
    __table_args__ = (
        PrimaryKeyConstraint('ID', 'CreatedDate', name='PK_PEEL_TEST_NAS'),
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    ItemCode: Mapped[str] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    LotNo: Mapped[str] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Type: Mapped[str] = mapped_column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    CreatedDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True, server_default=text('(getdate())'))
    Data: Mapped[Optional[str]] = mapped_column(Unicode(collation='SQL_Latin1_General_CP1_CI_AS'))
    LocationImg: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))


class Permissions(Base):
    __tablename__ = 'Permissions'
    __table_args__ = (
        PrimaryKeyConstraint('PermissionID', name='PK__Permissi__EFA6FB0F98629239'),
        Index('UQ__Permissi__91FE57503DD9CB62', 'PermissionCode', mssql_clustered=False, unique=True)
    )

    PermissionID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    PermissionCode: Mapped[str] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Description: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Roles: Mapped[list['Roles']] = relationship('Roles', secondary='RolePermissions', back_populates='Permissions_')


class Roles(Base):
    __tablename__ = 'Roles'
    __table_args__ = (
        PrimaryKeyConstraint('RoleID', name='PK__Roles__8AFACE3AE58C2679'),
        Index('UQ__Roles__8A2B61606C90715F', 'RoleName', mssql_clustered=False, unique=True)
    )

    RoleID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    RoleName: Mapped[str] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Description: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))

    Permissions_: Mapped[list['Permissions']] = relationship('Permissions', secondary='RolePermissions', back_populates='Roles')
    Users: Mapped[list['Users']] = relationship('Users', secondary='UserRoles', back_populates='Roles_')


class Users(Base):
    __tablename__ = 'Users'
    __table_args__ = (
        PrimaryKeyConstraint('UserIDI', name='PK_Users_UserIDI'),
        Index('UQ_Users_EmployeeID', 'EmployeeID', mssql_clustered=False, unique=True),
        Index('UQ_Users_UserID', 'UserID', mssql_clustered=False, unique=True),
        Index('UQ_Users_Username', 'Username', mssql_clustered=False, unique=True)
    )

    UserIDI: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    UserID: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, server_default=text('(newid())'))
    Username: Mapped[str] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    EmployeeID: Mapped[str] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    PasswordHash: Mapped[str] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UserStatus: Mapped[int] = mapped_column(TINYINT, nullable=False, server_default=text('((1))'))
    FailedLoginAttempts: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('((0))'))
    CreatedDateTimeUTC: Mapped[datetime.datetime] = mapped_column(DATETIME2, nullable=False, server_default=text('(sysutcdatetime())'))
    LastModifiedDateTimeUTC: Mapped[datetime.datetime] = mapped_column(DATETIME2, nullable=False, server_default=text('(sysutcdatetime())'))
    LastLoginDateTimeUTC: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME2)
    LastLoginIpAddress: Mapped[Optional[str]] = mapped_column(String(45, 'SQL_Latin1_General_CP1_CI_AS'))
    SecurityStamp: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, server_default=text('(newid())'))

    Roles_: Mapped[list['Roles']] = relationship('Roles', secondary='UserRoles', back_populates='Users')


t_RolePermissions = Table(
    'RolePermissions', Base.metadata,
    Column('RoleID', Integer, primary_key=True),
    Column('PermissionID', Integer, primary_key=True),
    ForeignKeyConstraint(['PermissionID'], ['Permissions.PermissionID'], ondelete='CASCADE', name='FK_RolePermissions_Permissions'),
    ForeignKeyConstraint(['RoleID'], ['Roles.RoleID'], ondelete='CASCADE', name='FK_RolePermissions_Roles'),
    PrimaryKeyConstraint('RoleID', 'PermissionID', name='PK_RolePermissions')
)


t_UserRoles = Table(
    'UserRoles', Base.metadata,
    Column('UserIDI', Integer, primary_key=True),
    Column('RoleID', Integer, primary_key=True),
    ForeignKeyConstraint(['RoleID'], ['Roles.RoleID'], ondelete='CASCADE', name='FK_UserRoles_Roles'),
    ForeignKeyConstraint(['UserIDI'], ['Users.UserIDI'], ondelete='CASCADE', name='FK_UserRoles_Users'),
    PrimaryKeyConstraint('UserIDI', 'RoleID', name='PK_UserRoles')
)
