# Backend Notes

## Dependencies

Install the backend dependencies (including Transformers, Torch, and pgvector helpers):

```bash
pip install -r requirements.txt
```

## Database Migrations

The pgvector extension is enabled via Alembic migrations. After updating your dependencies, run the migration:

```bash
alembic -c backend/alembic.ini upgrade head
```

This migration will create the `media_items` table (if needed), add the `embedding` vector column, and ensure the `pdq_hash` column and indexes exist.

## Duplicate Detection Pipeline

- **PDQ fallback** – If a native PDQ binding is unavailable, the `PDQFilter` will log a warning and fall back to `imagehash.pHash` for perceptual hashing. Install a PDQ-compatible library when available to avoid the fallback.
- **SigLIP-2 embeddings** – Embeddings are computed with the SigLIP-2 encoder provided by `transformers` and stored in Postgres using `pgvector`.

Useful Make targets:

```bash
make tests-dedupe  # runs the PDQ, encoder, and vector store unit tests
```
