from contextlib import asynccontextmanager

from dependency_injector import containers
from fastapi import FastAPI

from api.middlewares.exception_middlewares import app_global_exception_middleware
from api.routes import router_registration
from api.routes.router_registration import api_v1_router
from core.container import Container
from domain.schemas.exceptions import DuplicateAccountError
from services import auth_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    try:
        auth_service = container.auth_service()

        await auth_service.initADMIN()

        print("ADMIN khởi tạo thành công!")
    except DuplicateAccountError as e:
        print("ADMIN đã được khởi tạo")
    except Exception as e:
        print("Khởi tạo admin thất bại!")

    yield
    await container.redis_service().close()
    print("🛑 Hệ thống đang tắt...")

def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        title = "Identity Service API For OK2SHIP_2.0",
        description="Identity Service API For OK2SHIP_2.0 with fast API",
        version="26.0.0",
        contact={
            "name": "gitzno",
            "email": "hoangthuy.forjob@gmail.com",
        },
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    app_global_exception_middleware(app)
    app.container = container

    #nhúng router tổng vào
    app.include_router(router_registration.router, prefix="/api")

    #Router health check
    @app.get("/", tags=["Root"])
    def health_check():
        return {"status": "Hello World"}

    return app

app = create_app()