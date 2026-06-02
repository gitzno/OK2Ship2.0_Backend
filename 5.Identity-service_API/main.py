from dependency_injector import containers
from fastapi import FastAPI

from api.routes import router_registration
from api.routes.router_registration import api_v1_router
from core.container import Container


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
        redoc_url="/redoc"
    )

    app.container = container

    #nhúng router tổng vào
    app.include_router(router_registration.router, prefix="/api")

    #Router health check
    @app.get("/", tags=["Root"])
    def health_check():
        return {"status": "Hello World"}

    return app

app = create_app()