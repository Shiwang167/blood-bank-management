#!/bin/bash
# EC2 Instance Setup Script for BloodBridge Backend
# Amazon Linux 2023 / Amazon Linux 2

set -e  # Exit on error

echo "=========================================="
echo "BloodBridge Backend - Amazon Linux Setup"
echo "=========================================="

# Update system
echo "📦 Updating system packages..."
sudo yum update -y

# Install Python 3.11 and dependencies
echo "📦 Installing Python 3.11 and dependencies..."
sudo yum install -y python3.11 python3.11-pip python3.11-devel

# Install other dependencies
echo "📦 Installing Nginx, Git, and PostgreSQL client..."
sudo yum install -y nginx git postgresql15 gcc

# Create application user (ec2-user already exists on Amazon Linux)
echo "👤 Using ec2-user for application..."

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /home/ec2-user/bloodbank
sudo chown -R ec2-user:ec2-user /home/ec2-user/bloodbank

# Create log directories
echo "📁 Creating log directories..."
sudo mkdir -p /var/log/bloodbank
sudo chown -R ec2-user:ec2-user /var/log/bloodbank

sudo mkdir -p /var/run/bloodbank
sudo chown -R ec2-user:ec2-user /var/run/bloodbank

echo ""
echo "✅ Base system setup complete!"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Clone your repository:"
echo "   cd /home/ec2-user"
echo "   git clone https://github.com/YOUR_USERNAME/blood-bank-management.git bloodbank"
echo ""
echo "2. Setup Python environment:"
echo "   cd /home/ec2-user/bloodbank/backend"
echo "   python3.11 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install --upgrade pip"
echo "   pip install -r requirements.txt"
echo ""
echo "3. Configure environment:"
echo "   cp .env.example .env"
echo "   nano .env"
echo "   # Add your DATABASE_URL and other settings"
echo ""
echo "4. Run database migrations:"
echo "   python scripts/migrate_db.py"
echo ""
echo "5. Setup systemd service:"
echo "   sudo cp deploy/bloodbank.service /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable bloodbank"
echo "   sudo systemctl start bloodbank"
echo ""
echo "6. Setup Nginx:"
echo "   sudo cp deploy/nginx.conf /etc/nginx/conf.d/bloodbank.conf"
echo "   sudo nginx -t"
echo "   sudo systemctl enable nginx"
echo "   sudo systemctl start nginx"
echo ""
echo "=========================================="

# Configure firewall (Amazon Linux uses firewalld or iptables)
echo "🔒 Note: Configure security groups in AWS Console"
echo "    - Allow port 22 (SSH)"
echo "    - Allow port 80 (HTTP)"
echo "    - Allow port 443 (HTTPS)"
