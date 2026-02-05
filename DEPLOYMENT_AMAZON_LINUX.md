# Amazon Linux Deployment Guide - BloodBridge

Complete deployment guide for Amazon Linux 2023 / Amazon Linux 2.

---

## Prerequisites

- ✅ RDS PostgreSQL database created
- ✅ EC2 instance running Amazon Linux
- ✅ Security groups configured
- ✅ SSH key pair downloaded
- ✅ Code pushed to GitHub

---

## Step 1: Connect to EC2

```bash
# Set permissions on your key file
chmod 400 your-key.pem

# Connect to EC2 (replace with your EC2 public IP)
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

**Note:** Amazon Linux uses `ec2-user` (not `ubuntu`)

---

## Step 2: System Setup

### 2.1 Update System

```bash
sudo yum update -y
```

### 2.2 Install Python 3.11

```bash
# Install Python 3.11
sudo yum install -y python3.11 python3.11-pip python3.11-devel

# Verify installation
python3.11 --version
```

### 2.3 Install Dependencies

```bash
# Install Nginx, Git, PostgreSQL client, and build tools
sudo yum install -y nginx git postgresql15 gcc

# Verify installations
nginx -v
git --version
psql --version
```

---

## Step 3: Clone Your Repository

```bash
# Navigate to home directory
cd /home/ec2-user

# Clone your repository (replace with your GitHub URL)
git clone https://github.com/YOUR_USERNAME/blood-bank-management.git bloodbank

# Navigate to backend
cd bloodbank/backend
```

---

## Step 4: Setup Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

You should see all packages installing successfully.

---

## Step 5: Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit with your settings
nano .env
```

Add your configuration (replace with actual values):

```bash
FLASK_ENV=production
SECRET_KEY=your-very-secure-random-secret-key-change-this
PORT=5000

JWT_SECRET=your-very-secure-jwt-secret-change-this

# Replace with your RDS endpoint
DATABASE_URL=postgresql://dbadmin:your-password@your-rds-endpoint.rds.amazonaws.com:5432/bloodbank

# Replace with your EC2 public IP or domain
CORS_ORIGIN=http://your-ec2-public-ip

DONATION_INTERVAL_DAYS=90
LOW_STOCK_THRESHOLD=5
CRITICAL_STOCK_THRESHOLD=3
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## Step 6: Test Database Connection

```bash
# Test connection to RDS
psql "$DATABASE_URL"

# If successful, you'll see PostgreSQL prompt
# Type \q to exit
```

**If connection fails:**
- Check RDS security group allows EC2 security group
- Verify DATABASE_URL is correct
- Ensure RDS is in same VPC as EC2

---

## Step 7: Run Database Migrations

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run migrations
python scripts/migrate_db.py
```

You should see:
```
✅ Applied 001_initial_schema.sql
✅ All migrations completed successfully!
```

---

## Step 8: Create Log Directories

```bash
# Create log directories
sudo mkdir -p /var/log/bloodbank
sudo chown -R ec2-user:ec2-user /var/log/bloodbank

sudo mkdir -p /var/run/bloodbank
sudo chown -R ec2-user:ec2-user /var/run/bloodbank
```

---

## Step 9: Setup Systemd Service

```bash
cd /home/ec2-user/bloodbank/backend

# Copy the Amazon Linux service file
sudo cp deploy/bloodbank_amazon_linux.service /etc/systemd/system/bloodbank.service

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable bloodbank

# Start service
sudo systemctl start bloodbank

# Check status
sudo systemctl status bloodbank
```

You should see **"active (running)"** in green.

### View Logs

```bash
# View application logs
sudo journalctl -u bloodbank -f

# Press Ctrl+C to exit
```

---

## Step 10: Test Application

```bash
# Test health endpoint
curl http://localhost:5000/health

# Should return:
# {"status":"healthy","service":"BloodBridge API","database":"connected"}
```

---

## Step 11: Setup Nginx

### 11.1 Configure Nginx

```bash
cd /home/ec2-user/bloodbank/backend

# Edit nginx config to add your EC2 public IP
nano deploy/nginx.conf

# Change this line:
# server_name your-domain.com;
# To:
# server_name your-ec2-public-ip;

# Save: Ctrl+X, Y, Enter
```

### 11.2 Install Nginx Configuration

```bash
# Copy nginx config
sudo cp deploy/nginx.conf /etc/nginx/conf.d/bloodbank.conf

# Test nginx configuration
sudo nginx -t

# Should show: "syntax is ok" and "test is successful"
```

### 11.3 Start Nginx

```bash
# Enable nginx (start on boot)
sudo systemctl enable nginx

# Start nginx
sudo systemctl start nginx

# Check status
sudo systemctl status nginx
```

---

## Step 12: Verify Deployment

### 12.1 Test from EC2

```bash
# Test health endpoint through Nginx
curl http://localhost/health

# Should return database status
```

### 12.2 Test from Browser

Open your browser and go to:
```
http://your-ec2-public-ip/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "BloodBridge API",
  "database": "connected"
}
```

### 12.3 Test API Endpoints

```bash
# Register a user
curl -X POST http://your-ec2-public-ip/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "Test123!",
    "role": "donor",
    "blood_type": "A+"
  }'

# Login
curl -X POST http://your-ec2-public-ip/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

---

## Step 13: Deploy Frontend (Optional)

### Option A: Serve via Nginx

```bash
# On your local machine, build frontend
cd "C:\Users\Shiwa\OneDrive\Desktop\Blood Bank Anant\frontend"

# Update .env.production
# VITE_API_URL=http://your-ec2-public-ip/api

npm run build

# Upload to EC2
scp -i your-key.pem -r dist ec2-user@your-ec2-ip:/home/ec2-user/bloodbank/frontend-dist
```

On EC2, update Nginx config:

```bash
sudo nano /etc/nginx/conf.d/bloodbank.conf

# Add this location block before the /api/ location:
# location / {
#     root /home/ec2-user/bloodbank/frontend-dist;
#     try_files $uri $uri/ /index.html;
# }

sudo nginx -t
sudo systemctl reload nginx
```

---

## Useful Commands for Amazon Linux

### Application Management

```bash
# View logs
sudo journalctl -u bloodbank -f

# Restart application
sudo systemctl restart bloodbank

# Check status
sudo systemctl status bloodbank

# Stop application
sudo systemctl stop bloodbank

# Start application
sudo systemctl start bloodbank
```

### Nginx Management

```bash
# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Reload configuration (no downtime)
sudo systemctl reload nginx

# View error logs
sudo tail -f /var/log/nginx/error.log

# View access logs
sudo tail -f /var/log/nginx/access.log
```

### Database

```bash
# Connect to database
psql "$DATABASE_URL"

# Run migrations
cd /home/ec2-user/bloodbank/backend
source venv/bin/activate
python scripts/migrate_db.py
```

### System

```bash
# Check disk space
df -h

# Check memory
free -h

# Check running processes
ps aux | grep gunicorn

# Check listening ports
sudo netstat -tlnp | grep -E ':(80|443|5000)'
```

---

## Troubleshooting

### Application Won't Start

```bash
# Check logs
sudo journalctl -u bloodbank -n 50

# Check if virtual environment exists
ls -la /home/ec2-user/bloodbank/backend/venv

# Check if dependencies are installed
source /home/ec2-user/bloodbank/backend/venv/bin/activate
pip list
```

### Database Connection Issues

```bash
# Test connection
psql "$DATABASE_URL"

# Check environment variables
cat /home/ec2-user/bloodbank/backend/.env

# Check security groups in AWS Console
# RDS should allow EC2 security group on port 5432
```

### Nginx Issues

```bash
# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Test configuration
sudo nginx -t

# Check if nginx is running
sudo systemctl status nginx

# Check if port 80 is listening
sudo netstat -tlnp | grep :80
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R ec2-user:ec2-user /home/ec2-user/bloodbank
sudo chown -R ec2-user:ec2-user /var/log/bloodbank
sudo chown -R ec2-user:ec2-user /var/run/bloodbank
```

---

## Deployment Updates

When you update your code:

```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@your-ec2-ip

# Navigate to project
cd /home/ec2-user/bloodbank

# Pull latest changes
git pull origin main

# Activate virtual environment
cd backend
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Run migrations
python scripts/migrate_db.py

# Restart application
sudo systemctl restart bloodbank

# Check status
sudo systemctl status bloodbank
```

---

## Security Hardening

### 1. Setup HTTPS (Recommended)

```bash
# Install certbot
sudo yum install -y certbot python3-certbot-nginx

# Get SSL certificate (requires domain name)
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### 2. Configure Firewall (Optional)

Amazon Linux 2023 uses firewalld:

```bash
# Start firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Allow services
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# Reload
sudo firewall-cmd --reload

# Check rules
sudo firewall-cmd --list-all
```

**Note:** Security groups in AWS Console are usually sufficient.

---

## Key Differences: Amazon Linux vs Ubuntu

| Feature | Amazon Linux | Ubuntu |
|---------|-------------|--------|
| Package Manager | `yum` | `apt-get` |
| Default User | `ec2-user` | `ubuntu` |
| Python Install | `yum install python3.11` | `apt-get install python3.11` |
| PostgreSQL Client | `postgresql15` | `postgresql-client` |
| Service User | `ec2-user` | `ubuntu` |

---

## Quick Reference

```bash
# System update
sudo yum update -y

# Install packages
sudo yum install -y package-name

# Service management
sudo systemctl start|stop|restart|status service-name

# View logs
sudo journalctl -u service-name -f

# File editing
nano filename

# Change ownership
sudo chown -R ec2-user:ec2-user /path/to/directory
```

---

## Summary

✅ System updated and dependencies installed  
✅ Python 3.11 virtual environment created  
✅ Database migrations completed  
✅ Systemd service running  
✅ Nginx configured and running  
✅ Application accessible via HTTP  

**Your Blood Bank application is now deployed on Amazon Linux!** 🚀

For updates, just pull from git and restart the service.
