#!/bin/bash

echo "🚀 Setting up the project..."

# Install Node.js dependencies
echo "📦 Installing backend dependencies..."
cd backend || exit
npm install
npm install puppeteer dotenv fs-extra
cd ..

echo "📦 Installing frontend dependencies..."
cd frontend || exit
npm install
cd ..

# Install Python dependencies in virtual environment
echo "🐍 Setting up Python virtual environment for AI processing..."
cd ai-processing || exit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Build and start Docker containers
echo "🐳 Building Docker containers..."
docker compose up --build -d

echo "✅ Setup complete! Run 'docker ps' to verify running containers."
