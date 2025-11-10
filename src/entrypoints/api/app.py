from dishka import AsyncContainer, Provider, make_async_container
from dishka.integrations.fastapi import FastapiProvider
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from src.entrypoints.api.exceptions import set_exception_handlers
from src.entrypoints.api.health import health_router
from src.entrypoints.api.lifespan import lifespan
from src.entrypoints.api.middleware import RequestContextLogMiddleware
from src.shared.infra.core.logger import setup_logger


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(RequestContextLogMiddleware)


def make_container(*extra_providers: Provider) -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        *extra_providers,
    )


def setup_metrics(app: FastAPI) -> None:
    Instrumentator().instrument(app).expose(
        app,
        include_in_schema=False,
    )


def create_app() -> FastAPI:
    setup_logger()

    app = FastAPI(lifespan=lifespan)

    app.include_router(health_router)

    set_exception_handlers(app)

    setup_middlewares(app)

    setup_metrics(app)

    return app
