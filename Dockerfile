FROM python:3.12-slim

WORKDIR /app

# Install Python + system packages
RUN apt-get update && \
    apt-get install -y \
    curl wget gnupg2 \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libasound2 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libx11-xcb1 libxcb1 libxext6 libxfixes3 libgtk-3-0 \
    libxkbcommon0 libnspr4 libnss3 libexpat1 libdbus-1-3 libatspi2.0-0 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright + browsers
RUN pip install playwright && playwright install

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

COPY ./backend ./backend

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
