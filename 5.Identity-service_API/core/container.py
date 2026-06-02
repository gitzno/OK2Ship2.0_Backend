from dependency_injector import containers, providers

from core.database import get_db_session, async_session
from reponsitories.user_repository import UserRepository
from services.auth_service import AuthService
from services.token_service import TokenService


class Container(containers.DeclarativeContainer):


    wiring_config = containers.WiringConfiguration(packages=[
        "api.routes.v1"
    ])


    """
    providers.Factory: Mỗi lần bạn gọi, nó sẽ tạo ra một đối tượng mới tinh. (Rất hợp cho Repository và Service).

    providers.Singleton: Tạo ra duy nhất một đối tượng và dùng chung cho toàn bộ app. (Hợp cho các class cấu hình hệ thống).

    providers.Resource: Chuyên dùng để quản lý các tài nguyên cần thao tác Đóng/Mở (như kết nối Database, File, Network). 
    """
    session_factory = providers.Object(async_session)

    #Register Repository
    user_repository = providers.Factory(
        UserRepository,
        session_factory=session_factory  # <--- SỬA DÒNG NÀY
    )


    #Register Service
    token_service = providers.Singleton(TokenService)

    auth_service = providers.Singleton(AuthService, user_repo=user_repository,
        token_service=token_service)