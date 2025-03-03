#!/bin/bash

echo "🛑 Stopping and cleaning up Docker containers..."
docker compose down

echo "🧹 Removing unused Docker images..."
docker system prune -f

echo "✅ Cleanup complete!"
