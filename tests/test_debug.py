import pytest
from fastapi.routing import APIRoute

from backend.main import app


@pytest.mark.debug
def test_print_routes() -> None:
    rows: list[tuple[str, list[str]]] = []
    for r in app.routes:
        if isinstance(r, APIRoute):
            rows.append((r.path, sorted(r.methods)))
        else:
            # Non-API routes (Mounts/Static/etc.)—print a readable label
            rows.append((str(r), []))
    rows.sort(key=lambda t: t[0])
    for p, methods in rows:
        print(p, methods)
    # Just a sanity check so the test always "passes"
    assert any("/api/ingest" in p for p, _ in rows)
