# AWS Deployment Guide - BloodBridge Application

This guide walks you through deploying the BloodBridge application to AWS EC2 with PostgreSQL RDS.

## Prerequisites

- AWS Account with billing enabled
- AWS CLI installed and configured
- SSH key pair for EC2 access
- Basic knowledge of AWS console

---

## Step 1: Create RDS PostgreSQL Database

### 1.1 Navigate to RDS in AWS Console

1. Log into AWS Console
2. Search for "RDS" and click on RDS service
3. Click **"Create database"**

### 1.2 Configure Database

**Engine options:**
- Engine type: **PostgreSQL**
- Version: **PostgreSQL 15.x** (latest stable)

**Templates:**
- Select **"Free tier"** (for testing) or **"Production"** (for production use)

**Settings:**
- DB instance identifier: `bloodbank-db`
- Master username: `dbadmin` (or your choice)
- Master password: Create a strong password and **save it securely**

**Instance configuration:**
- DB instance class: `db.t3.micro` (Free tier) or `db.t3.small` (Production)

**Storage:**
- Allocated storage: 20 GB
- Enable storage autoscaling: Yes
- Maximum storage threshold: 100 GB

**Connectivity:**
- Virtual Private Cloud (VPC): Default VPC
- Public access: **Yes** (for initial setup; restrict later)
- VPC security group: Create new → Name it `bloodbank-db-sg`
- Availability Zone: No preference

**Database authentication:**
- Password authentication

**Additional configuration:**
- Initial database name: `bloodbank`
- Backup retention: 7 days
- Enable encryption: Yes (recommended)

### 1.3 Create Database

Click **"Create database"** and wait 5-10 minutes for the database to be created.

### 1.4 Configure Security Group

1. Go to **EC2 → Security Groups**
2. Find `bloodbank-db-sg`
3. Edit **Inbound rules**:
   - Type: PostgreSQL
   - Port: 5432
   - Source: Custom → (We'll add EC2 security group later)
   - Description: Allow from EC2

### 1.5 Get Database Endpoint

1. Go to RDS → Databases → `bloodbank-db`
2. Copy the **Endpoint** (looks like: `bloodbank-db.xxxxx.us-east-1.rds.amazonaws.com`)
3. Save this for later use

---

## Step 2: Create EC2 Instance

### 2.1 Launch EC2 Instance

1. Navigate to **EC2** in AWS Console
2. Click **"Launch Instance"**

### 2.2 Configure Instance

**Name:** `bloodbank-backend`

**Application and OS Images:**
- AMI: **Ubuntu Server 22.04 LTS**
- Architecture: 64-bit (x86)

**Instance type:**
- `t2.micro` (Free tier) or `t2.small` (Production)

**Key pair:**
- Create new key pair or use existing
- Name: `bloodbank-key`
- Type: RSA
- Format: `.pem` (for SSH)
- **Download and save the key file securely**

**Network settings:**
- VPC: Default VPC
- Auto-assign public IP: **Enable**
- Firewall (security groups): Create new
  - Name: `bloodbank-backend-sg`
  - Description: Security group for BloodBank backend
  - Inbound rules:
    - SSH (22) from My IP
    - HTTP (80) from Anywhere
    - HTTPS (443) from Anywhere

**Storage:**
- 20 GB gp3 (General Purpose SSD)

### 2.3 Launch Instance

Click **"Launch instance"** and wait for it to start.

### 2.4 Update RDS Security Group

1. Go to **EC2 → Security Groups → bloodbank-db-sg**
2. Edit **Inbound rules**
3. Add rule:
   - Type: PostgreSQL
   - Port: 5432
   - Source: Custom → Select `bloodbank-backend-sg`
   - Save rules

---

## Step 3: Connect to EC2 and Setup

### 3.1 Connect via SSH

```bash
# Set permissions on your key file
chmod 400 bloodbank-key.pem

# Connect to EC2 (replace with your EC2 public IP)
ssh -i bloodbank-key.pem ubuntu@your-ec2-public-ip
```

### 3.2 Run Initial Setup

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3.11 python3.11-venv python3-pip nginx git postgresql-client build-essential libpq-dev

# Create application directory
sudo mkdir -p /home/ubuntu/bloodbank
sudo chown -R ubuntu:ubuntu /home/ubuntu/bloodbank

# Create log directories
sudo mkdir -p /var/log/bloodbank /var/run/bloodbank
sudo chown -R ubuntu:ubuntu /var/log/bloodbank /var/run/bloodbank
```

### 3.3 Upload Application Code

**Option A: Using Git (Recommended)**
```bash
cd /home/ubuntu/bloodbank
git clone YOUR_REPOSITORY_URL .
```

**Option B: Using SCP from your local machine**
```bash
# From your local machine
scp -i bloodbank-key.pem -r "C:\Users\Shiwa\OneDrive\Desktop\Blood Bank Anant\backend" ubuntu@your-ec2-ip:/home/ubuntu/bloodbank/
```

### 3.4 Setup Python Environment

```bash
cd /home/ubuntu/bloodbank/backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.5 Configure Environment Variables

```bash
cd /home/ubuntu/bloodbank/backend

# Create .env file
nano .env
```

Add the following (replace with your actual values):

```bash
FLASK_ENV=production
SECRET_KEY=your-very-secure-random-secret-key-here
PORT=5000

JWT_SECRET=your-very-secure-jwt-secret-here

# Replace with your RDS endpoint and credentials
DATABASE_URL=postgresql://dbadmin:your-password@bloodbank-db.xxxxx.us-east-1.rds.amazonaws.com:5432/bloodbank

CORS_ORIGIN=http://your-ec2-public-ip,https://your-domain.com

DONATION_INTERVAL_DAYS=90
LOW_STOCK_THRESHOLD=5
CRITICAL_STOCK_THRESHOLD=3
```

Save and exit (Ctrl+X, Y, Enter)

---

## Step 4: Initialize Database

### 4.1 Test Database Connection

```bash
# Test connection to RDS
psql "$DATABASE_URL"

# If successful, you'll see PostgreSQL prompt
# Type \q to exit
```

### 4.2 Run Database Migrations

```bash
cd /home/ubuntu/bloodbank/backend
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

## Step 5: Setup Systemd Service

### 5.1 Install Service File

```bash
cd /home/ubuntu/bloodbank/backend

# Copy service file
sudo cp deploy/bloodbank.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable bloodbank

# Start service
sudo systemctl start bloodbank

# Check status
sudo systemctl status bloodbank
```

You should see "active (running)" in green.

### 5.2 View Logs

```bash
# View application logs
sudo journalctl -u bloodbank -f

# Press Ctrl+C to exit
```

---

## Step 6: Setup Nginx

### 6.1 Configure Nginx

```bash
cd /home/ubuntu/bloodbank/backend

# Edit nginx config and replace 'your-domain.com' with your EC2 public IP
sudo nano deploy/nginx.conf
# Change: server_name your-domain.com;
# To: server_name your-ec2-public-ip;

# Copy nginx config
sudo cp deploy/nginx.conf /etc/nginx/sites-available/bloodbank

# Create symbolic link
sudo ln -s /etc/nginx/sites-available/bloodbank /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### 6.2 Verify Backend is Running

```bash
# Test health endpoint
curl http://localhost:5000/health

# Should return:
# {"status":"healthy","service":"BloodBridge API","database":"connected"}
```

---

## Step 7: Deploy Frontend

### 7.1 Build Frontend Locally

On your local machine:

```bash
cd "C:\Users\Shiwa\OneDrive\Desktop\Blood Bank Anant\frontend"

# Update .env.production with your EC2 IP
# VITE_API_URL=http://your-ec2-public-ip/api

# Build for production
npm run build
```

### 7.2 Upload to EC2

**Option A: Serve via Nginx (Simple)**

```bash
# From local machine
scp -i bloodbank-key.pem -r dist ubuntu@your-ec2-ip:/home/ubuntu/bloodbank/frontend-dist
```

On EC2, update Nginx config:

```bash
sudo nano /etc/nginx/sites-available/bloodbank
```

Add this location block:

```nginx
# Serve frontend
location / {
    root /home/ubuntu/bloodbank/frontend-dist;
    try_files $uri $uri/ /index.html;
}
```

Restart Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

**Option B: Deploy to S3 + CloudFront (Recommended for Production)**

See AWS documentation for S3 static website hosting.

---

## Step 8: Verification

### 8.1 Test Backend API

```bash
# From your local machine or browser

# Health check
curl http://your-ec2-public-ip/health

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

### 8.2 Test Frontend

Open browser and navigate to:
```
http://your-ec2-public-ip
```

Test:
- User registration
- Login
- Create blood request
- View inventory

---

## Step 9: Production Hardening (Recommended)

### 9.1 Setup HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate (requires domain name)
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### 9.2 Restrict RDS Access

1. Go to RDS Security Group
2. Remove "Anywhere" access
3. Only allow from EC2 security group

### 9.3 Setup CloudWatch Monitoring (Optional)

- Enable detailed monitoring in EC2
- Create CloudWatch alarms for CPU, memory, disk
- Setup log groups for application logs

### 9.4 Setup Automated Backups

- RDS automated backups (already enabled)
- Create AMI snapshot of EC2 instance
- Setup S3 bucket for application backups

---

## Troubleshooting

### Database Connection Issues

```bash
# Test from EC2
psql "$DATABASE_URL"

# Check security groups
# Ensure EC2 security group is allowed in RDS security group
```

### Application Not Starting

```bash
# Check logs
sudo journalctl -u bloodbank -n 50

# Check if port 5000 is listening
sudo netstat -tlnp | grep 5000

# Restart service
sudo systemctl restart bloodbank
```

### Nginx Issues

```bash
# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

---

## Useful Commands

```bash
# View application logs
sudo journalctl -u bloodbank -f

# Restart application
sudo systemctl restart bloodbank

# Check application status
sudo systemctl status bloodbank

# Restart Nginx
sudo systemctl restart nginx

# Connect to database
psql "$DATABASE_URL"

# Run new migrations
cd /home/ubuntu/bloodbank/backend
source venv/bin/activate
python scripts/migrate_db.py
```

---

## Cost Estimation

**Monthly AWS Costs (Approximate):**

- EC2 t2.micro: $8-10/month
- RDS db.t3.micro: $15-20/month
- Data transfer: $5-10/month
- **Total: ~$30-40/month**

For production with larger instances:
- EC2 t2.small: $15-20/month
- RDS db.t3.small: $30-40/month
- **Total: ~$50-70/month**

---

## Next Steps

1. ✅ Setup domain name (optional but recommended)
2. ✅ Configure HTTPS with SSL certificate
3. ✅ Setup monitoring and alerts
4. ✅ Configure automated backups
5. ✅ Implement CI/CD pipeline (GitHub Actions, etc.)
6. ✅ Add application logging and monitoring
7. ✅ Setup staging environment

---

## Support

For issues or questions:
- Check application logs: `sudo journalctl -u bloodbank -f`
- Check nginx logs: `sudo tail -f /var/log/nginx/error.log`
- Verify database connectivity: `psql "$DATABASE_URL"`
