#!/bin/bash
# Deployment Script for BloodBridge Backend
# Run this script to deploy updates to the application

set -e  # Exit on error

APP_DIR="/home/ubuntu/bloodbank/backend"
VENV_DIR="$APP_DIR/venv"

echo "=========================================="
echo "BloodBridge Backend - Deployment"
echo "=========================================="

# Navigate to app directory
cd $APP_DIR

# Pull latest code (if using git)
# echo "📥 Pulling latest code..."
# git pull origin main

echo "🔄 Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
python scripts/migrate_db.py

# Collect static files (if any)
# python manage.py collectstatic --noinput

# Restart the application
echo "🔄 Restarting application..."
sudo systemctl restart bloodbank

# Wait a moment for the service to start
sleep 3

# Check service status
echo "🔍 Checking service status..."
sudo systemctl status bloodbank --no-pager

# Test health endpoint
echo "🏥 Testing health endpoint..."
sleep 2
curl -f http://localhost:5000/health || echo "⚠️  Health check failed"

echo ""
echo "✅ Deployment complete!"
echo "Check logs with: sudo journalctl -u bloodbank -f"
