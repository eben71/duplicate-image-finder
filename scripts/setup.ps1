Write-Host "🚀 Setting up the project..."

# Install Node.js dependencies
Write-Host "📦 Installing backend dependencies..."
Set-Location backend
npm install
Set-Location ..

Write-Host "📦 Installing frontend dependencies..."
Set-Location frontend
npm install
Set-Location ..

# Install Python dependencies in virtual environment
Write-Host "🐍 Setting up Python virtual environment for AI processing..."
Set-Location ai-processing
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
Set-Location ..

# Build and start Docker containers
Write-Host "🐳 Building Docker containers..."
docker compose up --build -d

Write-Host "✅ Setup complete! Run 'docker ps' to verify running containers."
