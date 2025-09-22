from types import TracebackType

import pytest

from backend.db import session as session_module


def test_get_session_uses_context_manager(monkeypatch: pytest.MonkeyPatch) -> None:
    events: list[str] = []
    sentinel_engine = object()

    class DummySession:
        def __init__(self, engine: object) -> None:
            assert engine is sentinel_engine

        def __enter__(self) -> "DummySession":
            events.append("enter")
            return self

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc: BaseException | None,
            tb: TracebackType | None,
        ) -> None:
            events.append("exit")

    monkeypatch.setattr(session_module, "Session", DummySession)
    monkeypatch.setattr(session_module, "engine", sentinel_engine)

    generator = session_module.get_session()
    produced = next(generator)
    assert isinstance(produced, DummySession)

    generator.close()
    assert events == ["enter", "exit"]
