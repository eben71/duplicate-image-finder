from types import TracebackType

from fastapi import FastAPI


class LifespanManager:
    """Minimal async context manager to drive FastAPI lifespan events in tests."""

    def __init__(self, app: FastAPI):
        self._context = app.router.lifespan_context(app)

    async def __aenter__(self) -> None:
        await self._context.__aenter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self._context.__aexit__(exc_type, exc, tb)
