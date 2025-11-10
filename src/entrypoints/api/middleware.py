import time
import uuid
from http import HTTPStatus

import structlog
from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = structlog.get_logger()


class RequestContextLogMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.perf_counter()
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        headers = Headers(scope=scope)
        request_id = headers.get("x-request-id", str(uuid.uuid4()))

        method = scope["method"]
        path = scope["path"]

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id, method=method, path=path
        )

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code

            if message["type"] == "http.response.start":
                status_code = message["status"]
                MutableHeaders(scope=message)["x-request-id"] = request_id

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception:
            process_time = time.perf_counter() - start_time

            logger.exception(
                "http_request_failed",
                status_code=status_code,
                duration_seconds=round(process_time, 4),
            )
            raise
        else:
            process_time = time.perf_counter() - start_time

            logger.info(
                "http_request_finished",
                status_code=status_code,
                duration_seconds=round(process_time, 4),
            )
        finally:
            structlog.contextvars.clear_contextvars()
