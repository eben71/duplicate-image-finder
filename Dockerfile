# mcr.microsoft.com/playwright/python
# https://mcr.microsoft.com/en-us/artifact/mar/playwright/python
# https://github.com/microsoft/playwright-python/releases
FROM mcr.microsoft.com/playwright/python:v1.53.0

WORKDIR /app

# Copy only requirements.txt first for caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set PYTHONPATH early for everything
ENV PYTHONPATH=/app

# Copy application code last to avoid invalidating dependency layer
COPY ./backend ./backend

# Default command (overridden in docker-compose)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
