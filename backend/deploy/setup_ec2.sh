#!/bin/bash
# EC2 Instance Setup Script for BloodBridge Backend
# Run this script on a fresh Ubuntu 22.04 EC2 instance

set -e  # Exit on error

echo "=========================================="
echo "BloodBridge Backend - EC2 Setup"
echo "=========================================="

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
echo "📦 Installing Python, Nginx, and other dependencies..."
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    nginx \
    git \
    postgresql-client \
    build-essential \
    libpq-dev

# Create application user (if not exists)
if ! id -u ubuntu &>/dev/null; then
    echo "👤 Creating ubuntu user..."
    sudo useradd -m -s /bin/bash ubuntu
fi

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /home/ubuntu/bloodbank
sudo chown -R ubuntu:ubuntu /home/ubuntu/bloodbank

# Create log directories
echo "📁 Creating log directories..."
sudo mkdir -p /var/log/bloodbank
sudo chown -R ubuntu:ubuntu /var/log/bloodbank

sudo mkdir -p /var/run/bloodbank
sudo chown -R ubuntu:ubuntu /var/run/bloodbank

# Clone repository (you'll need to replace with your repo URL)
echo "📥 Cloning repository..."
cd /home/ubuntu/bloodbank
# git clone YOUR_REPO_URL .
# For now, you'll need to manually upload your code

echo ""
echo "⚠️  MANUAL STEPS REQUIRED:"
echo "1. Upload your backend code to /home/ubuntu/bloodbank/backend"
echo "2. Create .env file with your configuration"
echo "3. Run the following commands:"
echo ""
echo "   cd /home/ubuntu/bloodbank/backend"
echo "   python3.11 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo ""
echo "4. Run database migrations:"
echo "   DATABASE_URL='your-rds-url' python scripts/migrate_db.py"
echo ""
echo "5. Setup systemd service:"
echo "   sudo cp deploy/bloodbank.service /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable bloodbank"
echo "   sudo systemctl start bloodbank"
echo ""
echo "6. Setup Nginx:"
echo "   sudo cp deploy/nginx.conf /etc/nginx/sites-available/bloodbank"
echo "   sudo ln -s /etc/nginx/sites-available/bloodbank /etc/nginx/sites-enabled/"
echo "   sudo nginx -t"
echo "   sudo systemctl restart nginx"
echo ""

# Configure firewall
echo "🔒 Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

echo ""
echo "✅ Base setup complete!"
echo "Follow the manual steps above to complete the deployment."
