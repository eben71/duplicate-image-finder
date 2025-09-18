FROM python:3.12-slim

WORKDIR /app

# Copy dependency manifests first for caching
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements-dev.txt

# Set PYTHONPATH early for everything
ENV PYTHONPATH=/app

# Copy application code last to avoid invalidating dependency layer
COPY ./backend ./backend

# Default command (overridden in docker-compose)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
