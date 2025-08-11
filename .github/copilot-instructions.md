# Copilot Review Instructions

## Context

- Stack: FastAPI + SQLModel; Celery/Redis; Postgres; Docker Compose. Frontend: Next.js later.
- Layout: routes → `backend/api/`; services → `backend/services/`; DB session/engine → `backend/db/session.py`.
- Privacy rules: never store original photos; only low-res proxies, hashes, embeddings.

## What to focus on in PR reviews

1. **Correctness & safety**
   - Token handling (encryption/refresh) untouched unless tests prove safety.
   - No secrets in code or logs. No new scopes without justification.
2. **Tests**
   - API tests use `httpx.AsyncClient`.
   - Coverage must not drop; suggest missing edge-case tests.
3. **Error handling & logging**
   - Return helpful errors; no bare `except`.
   - Ensure `trace_id` is logged through calls.
4. **Performance**
   - No O(N^2) across full libraries; batching of similarity steps.
5. **Scope creep**
   - No new infrastructure/services without an issue explaining the risk it solves.

## Don’t suggest

- Auto-delete user photos.
- Storing EXIF/PII except what’s documented.
- Adding heavy deps or new services without rationale.

## Definition of Done for changes

- Tests added/updated; CI green; coverage unchanged or up.
- Ruff/Black clean; docstrings added where logic is non-trivial.
