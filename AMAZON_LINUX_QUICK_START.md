# Amazon Linux Deployment - Quick Start

## ✅ You're Using Amazon Linux!

Perfect! Here are the Amazon Linux specific commands for your deployment.

---

## 🚀 Quick Deployment (Copy & Paste)

### Step 1: Connect to EC2

```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

**Note:** Use `ec2-user` (not `ubuntu`)

### Step 2: Run All Setup Commands

```bash
# Update system
sudo yum update -y

# Install dependencies
sudo yum install -y python3.11 python3.11-pip python3.11-devel nginx git postgresql15 gcc

# Clone repository (replace YOUR_USERNAME)
cd /home/ec2-user
git clone https://github.com/YOUR_USERNAME/blood-bank-management.git bloodbank

# Setup Python environment
cd bloodbank/backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env
```

**In nano editor, add:**
```bash
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key
JWT_SECRET=your-jwt-secret
DATABASE_URL=postgresql://dbadmin:your-password@your-rds-endpoint.rds.amazonaws.com:5432/bloodbank
CORS_ORIGIN=http://your-ec2-public-ip
```

**Save:** `Ctrl+X`, `Y`, `Enter`

```bash
# Create log directories
sudo mkdir -p /var/log/bloodbank /var/run/bloodbank
sudo chown -R ec2-user:ec2-user /var/log/bloodbank /var/run/bloodbank

# Run database migrations
python scripts/migrate_db.py

# Setup systemd service
sudo cp deploy/bloodbank_amazon_linux.service /etc/systemd/system/bloodbank.service
sudo systemctl daemon-reload
sudo systemctl enable bloodbank
sudo systemctl start bloodbank

# Check application status
sudo systemctl status bloodbank

# Setup Nginx
# First, edit nginx.conf to add your EC2 IP
nano deploy/nginx.conf
# Change: server_name your-domain.com;
# To: server_name your-ec2-public-ip;
# Save: Ctrl+X, Y, Enter

sudo cp deploy/nginx.conf /etc/nginx/conf.d/bloodbank.conf
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl start nginx

# Test deployment
curl http://localhost/health
```

---

## ✅ Verification

### Test API Health
```bash
curl http://your-ec2-public-ip/health
```

Should return:
```json
{"status":"healthy","service":"BloodBridge API","database":"connected"}
```

### Test User Registration
```bash
curl -X POST http://your-ec2-public-ip/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@test.com","password":"Test123!","role":"donor","blood_type":"A+"}'
```

---

## 📚 Documentation

- **[DEPLOYMENT_AMAZON_LINUX.md](file:///C:/Users/Shiwa/OneDrive/Desktop/Blood%20Bank%20Anant/DEPLOYMENT_AMAZON_LINUX.md)** - Complete step-by-step guide
- **[AMAZON_LINUX_COMMANDS.md](file:///C:/Users/Shiwa/OneDrive/Desktop/Blood%20Bank%20Anant/AMAZON_LINUX_COMMANDS.md)** - Quick command reference

---

## 🔑 Key Differences from Ubuntu

| Item | Ubuntu | Amazon Linux |
|------|--------|--------------|
| Package Manager | `apt-get` | `yum` |
| User | `ubuntu` | `ec2-user` |
| Update | `sudo apt-get update` | `sudo yum update -y` |
| Install | `sudo apt-get install -y` | `sudo yum install -y` |
| PostgreSQL | `postgresql-client` | `postgresql15` |

---

## 🛠️ Common Commands

```bash
# View logs
sudo journalctl -u bloodbank -f

# Restart application
sudo systemctl restart bloodbank

# Restart Nginx
sudo systemctl restart nginx

# Check status
sudo systemctl status bloodbank

# Test database
psql "$DATABASE_URL"
```

---

## 🔧 Troubleshooting

**Application won't start:**
```bash
sudo journalctl -u bloodbank -n 50
```

**Database connection issues:**
```bash
# Test connection
psql "$DATABASE_URL"

# Check security groups in AWS Console
# RDS should allow EC2 security group on port 5432
```

**Nginx errors:**
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

---

## 📝 Files Created for Amazon Linux

✅ `backend/deploy/setup_ec2_amazon_linux.sh` - Setup script  
✅ `backend/deploy/bloodbank_amazon_linux.service` - Systemd service  
✅ `DEPLOYMENT_AMAZON_LINUX.md` - Complete guide  
✅ `AMAZON_LINUX_COMMANDS.md` - Quick reference  

---

**You're all set for Amazon Linux deployment!** 🚀

Follow the commands above to deploy your Blood Bank application.
