from typing import Optional
import datetime
import uuid

from sqlalchemy import DateTime, Identity, Index, Integer, PrimaryKeyConstraint, String, Unicode, Uuid, text
from sqlalchemy.dialects.mssql import DATETIME2, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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
