import pytest
from asgi_lifespan import LifespanManager
from dishka.integrations.fastapi import setup_dishka
from httpx import ASGITransport, AsyncClient
from src.entrypoints.api.app import create_app, make_container


@pytest.fixture(scope="session")
async def container():
    return make_container()


@pytest.fixture(scope="session")
async def app(container):
    app = create_app()
    setup_dishka(container, app)
    return app


@pytest.fixture(scope="session")
async def client(app):
    async with LifespanManager(app) as manager:
        transport = ASGITransport(app=manager.app)

        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c
