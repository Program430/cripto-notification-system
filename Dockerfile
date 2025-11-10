FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/


FROM base AS runtime

RUN poetry install --only main --no-root

COPY src /app/src

CMD ["uvicorn", "src.entrypoints.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log", "--log-level", "info"]


FROM base AS dev

RUN poetry install --with dev --no-root

COPY src /app/src

CMD ["uvicorn", "src.entrypoints.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--no-access-log", "--log-level", "debug"]