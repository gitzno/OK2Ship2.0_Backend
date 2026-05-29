import pyodbc
from dependency_injector import providers, containers

from src.adapters.services.bcrypt_hasher import BcryptHasher
from src.adapters.services.jwt_service import JWTService
from src.infrastructure.config import settings


def make_db_connection() -> pyodbc.Connection:
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={settings.DB_HOST},{settings.DB_PORT};"
        f"DATABASE={settings.DB_NAME};"
        f"UID={settings.DB_USER};"
        f"PWD={settings.DB_PASSWORD};"
        f"Encrypt=yes;TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)

class AppContainer(containers.DeclarativeContainer):

    #1.Cấu hình các file sẽ được tiêm DI tự động
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.infrastructure.api.v1.auth_routes",
        ]
    )

    #2. Quản lý kết nối database
    db_connection = providers.Resource(make_db_connection())

    #3. Khai báo singleton
    token_service = providers.Singleton(JWTService)
    password_hasher = providers.Singleton(BcryptHasher)



