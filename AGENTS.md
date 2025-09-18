# AGENTS.md

## Purpose
This file guides CODEX reviewers working on pull requests for the Duplicate Image Finder project. The goal is consistent, high-quality reviews that protect OAuth flows, data security, and ingestion reliability.

## System Snapshot
- **FastAPI backend** (`backend/`) with SQLModel + Alembic, integrates Google Photos OAuth and ingestion.
- **Core utilities** (`core/`) for cryptography, logging, and Google OAuth helpers.
- **Celery worker** (`backend/services/worker/`) generating embeddings asynchronously.
- **Frontend stub** (`frontend/`) served separately; most PRs focus on backend/core.
- **Tests** under `tests/` (unit & integration) with pytest + respx + async fixtures.

## Review Priorities
1. **Security & Secrets**
   - Validate encryption (`core/crypto.py`) and token handling—never leak plaintext secrets or store unencrypted values.
   - Check Google OAuth logic (`core/google_oauth.py`, `backend/api/routes.py`) for correct refresh handling, HTTP methods, and error propagation.
2. **Data Integrity**
   - Ensure SQLModel schemas, Alembic migrations, and Session usage remain consistent.
   - Confirm background tasks (`backend/services/worker/tasks.py`) keep DB sessions clean.
3. **Async + HTTP Correctness**
   - Watch for improper `await` usage with `httpx.Response` helpers, incorrect HTTP verbs, missing timeouts, or ignoring `raise_for_status()`.
4. **Configuration & Logging**
   - Settings live in `backend/config/settings.py`; verify new env vars have defaults or validation.
   - Logging should respect `core/logging_config.configure_logging()` and avoid duplicate `basicConfig` calls.
5. **Testing Discipline**
   - Expect new or modified behavior to include tests in `tests/` with clear async mocks (respx/AsyncMock) and DB fixture usage.

## Review Workflow
- **Scope first**: Skim PR description, verify linked issues, and inspect touched files to understand intent.
- **Static thinking**: Trace code paths for regressions, security leaks, concurrency issues, and data races.
- **Cross-check configuration**: Ensure new settings or env vars are documented (`README.md`, `.env.example`, `settings.py`).
- **Database focus**: For model changes, require matching Alembic migration and test coverage.
- **Background workers**: Verify Celery tasks stay idempotent, handle retries, and close sessions.
- **Frontend updates**: Confirm API contracts stay compatible (response shapes, status codes) and update shared schemas as needed.

## Testing Expectations
- Run or request `pytest` where feasible (`make tests` or `pytest`).
- For OAuth integrations, prefer respx or AsyncMock-based tests over live calls.
- When logic touches DB state, ensure fixtures create/cleanup SQLModel metadata.
- If a PR cannot be tested (e.g., missing env or external service), document why and suggest alternatives.

## Common Pitfalls to Flag
- Forgetting to reset `requires_reauth` on successful token refresh/login.
- Using POST instead of GET for Google userinfo, or awaiting synchronous `response.json()`.
- Not preserving existing refresh tokens when Google omits them on refresh.
- Setting mutable default arguments or sharing sessions across async contexts.
- Introducing migrations without updating SQLModel models (and vice versa).
- Logging secrets or creating duplicate logger configuration.

## Review Output Style
- Lead with high-severity findings (security, data loss, or runtime breakages) referencing `path:line`.
- Use clear severity labels (High/Medium/Low) and explain risk + fix suggestion.
- Highlight missing tests or documentation updates explicitly.
- Close with outstanding questions or confirmation that blockers are resolved.

## Ready-to-Merge Checklist
- [ ] All blocking findings addressed or explained.
- [ ] Tests added/updated and passing locally or in CI.
- [ ] Migrations (if any) align with model changes.
- [ ] Docs/config refreshed for new settings or behaviors.
- [ ] Secrets remain encrypted and OAuth flows are healthy.
