from dishka.integrations.fastapi import setup_dishka
from src.entrypoints.api.app import create_app, make_container

app = create_app()
container = make_container()
setup_dishka(container, app)
