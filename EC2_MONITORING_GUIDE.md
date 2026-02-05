# EC2 Backend & Database Monitoring Guide

## 🔍 Quick Health Checks

### **1. Check Backend Service Status**

```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@43.204.234.177

# Check if backend service is running
sudo systemctl status bloodbank

# Expected output:
# ● bloodbank.service - BloodBridge Flask Application
#    Loaded: loaded
#    Active: active (running)
```

**Status Indicators:**
- ✅ `active (running)` - Service is working
- ❌ `inactive (dead)` - Service stopped
- ❌ `failed` - Service crashed

---

### **2. Check Backend Logs**

```bash
# View last 50 lines of logs
sudo journalctl -u bloodbank -n 50

# Follow logs in real-time (Ctrl+C to exit)
sudo journalctl -u bloodbank -f

# Check for errors only
sudo journalctl -u bloodbank -p err -n 20
```

**What to look for:**
- ✅ "Running on http://0.0.0.0:5000"
- ✅ "Database connection successful"
- ❌ "Connection refused"
- ❌ "Error" or "Exception"

---

### **3. Test Backend API Directly**

```bash
# Test health endpoint
curl http://localhost:5000/health

# Expected response:
# {"status":"healthy","service":"BloodBridge API","database":"connected"}

# Test from outside EC2
curl http://43.204.234.177/health
```

---

### **4. Check Database Connection**

```bash
# Navigate to backend directory
cd /home/ec2-user/bloodbank/backend

# Check .env file (verify DATABASE_URL)
cat .env | grep DATABASE_URL

# Test database connection directly
source venv/bin/activate
python3 << EOF
from config import config
from services import RDSService

cfg = config['production']()
db = RDSService(cfg)
if db.health_check():
    print("✅ Database connection successful!")
else:
    print("❌ Database connection failed!")
EOF
```

---

### **5. Connect to PostgreSQL Database**

```bash
# Get database URL from .env
cat .env | grep DATABASE_URL

# Connect to database (will prompt for password)
psql "postgresql://dbadmin:YOUR_PASSWORD@YOUR_RDS_ENDPOINT:5432/bloodbank"

# Once connected, run these commands:
\dt                    # List all tables
\d users              # Describe users table
SELECT COUNT(*) FROM users;           # Count users
SELECT * FROM users LIMIT 5;          # View first 5 users
SELECT * FROM blood_requests LIMIT 5; # View requests
\q                    # Quit
```

---

### **6. Check Nginx Status**

```bash
# Check Nginx service
sudo systemctl status nginx

# Test Nginx configuration
sudo nginx -t

# View Nginx access logs
sudo tail -f /var/log/nginx/access.log

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

---

### **7. Check Running Processes**

```bash
# Check if Gunicorn workers are running
ps aux | grep gunicorn

# Expected output: Multiple gunicorn processes

# Check listening ports
sudo netstat -tlnp | grep -E ':(80|443|5000)'

# Expected:
# :80   - Nginx
# :5000 - Gunicorn/Flask
```

---

### **8. Check System Resources**

```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Press 'q' to exit top
```

---

## 🔧 Common Troubleshooting Commands

### **Backend Not Running:**

```bash
# Start the service
sudo systemctl start bloodbank

# Check status
sudo systemctl status bloodbank

# View recent errors
sudo journalctl -u bloodbank -n 50
```

---

### **Database Connection Issues:**

```bash
# Test database connectivity
cd /home/ec2-user/bloodbank/backend
source venv/bin/activate

# Check if DATABASE_URL is correct
cat .env | grep DATABASE_URL

# Test connection
psql "$DATABASE_URL"
```

**Common Issues:**
- ❌ Connection timeout → Check RDS security group
- ❌ Authentication failed → Wrong password in DATABASE_URL
- ❌ Database not found → Wrong database name

---

### **Restart Services:**

```bash
# Restart backend
sudo systemctl restart bloodbank

# Restart Nginx
sudo systemctl restart nginx

# Check both are running
sudo systemctl status bloodbank
sudo systemctl status nginx
```

---

## 📊 Complete Health Check Script

Save this as `health-check.sh`:

```bash
#!/bin/bash

echo "=== BloodBridge Health Check ==="
echo ""

# 1. Backend Service
echo "1. Backend Service Status:"
sudo systemctl is-active bloodbank
echo ""

# 2. Nginx Service
echo "2. Nginx Service Status:"
sudo systemctl is-active nginx
echo ""

# 3. Backend API Health
echo "3. Backend API Health:"
curl -s http://localhost:5000/health | python3 -m json.tool
echo ""

# 4. Database Connection
echo "4. Database Connection:"
cd /home/ec2-user/bloodbank/backend
source venv/bin/activate
python3 -c "
from config import config
from services import RDSService
cfg = config['production']()
db = RDSService(cfg)
if db.health_check():
    print('✅ Database: Connected')
else:
    print('❌ Database: Disconnected')
"
echo ""

# 5. Disk Space
echo "5. Disk Space:"
df -h / | tail -1
echo ""

# 6. Memory Usage
echo "6. Memory Usage:"
free -h | grep Mem
echo ""

# 7. Recent Errors
echo "7. Recent Backend Errors:"
sudo journalctl -u bloodbank -p err -n 5 --no-pager
echo ""

echo "=== Health Check Complete ==="
```

**Run it:**
```bash
chmod +x health-check.sh
./health-check.sh
```

---

## 📋 Quick Reference Commands

| Task | Command |
|------|---------|
| **Check backend status** | `sudo systemctl status bloodbank` |
| **View backend logs** | `sudo journalctl -u bloodbank -f` |
| **Restart backend** | `sudo systemctl restart bloodbank` |
| **Test API** | `curl http://localhost:5000/health` |
| **Connect to database** | `psql "$DATABASE_URL"` |
| **Check Nginx** | `sudo systemctl status nginx` |
| **View Nginx logs** | `sudo tail -f /var/log/nginx/error.log` |
| **Check disk space** | `df -h` |
| **Check memory** | `free -h` |

---

## 🎯 Quick Diagnostic Steps

**If backend is not responding:**

1. Check service status: `sudo systemctl status bloodbank`
2. View logs: `sudo journalctl -u bloodbank -n 50`
3. Restart service: `sudo systemctl restart bloodbank`
4. Test API: `curl http://localhost:5000/health`

**If database connection fails:**

1. Check .env: `cat /home/ec2-user/bloodbank/backend/.env`
2. Test connection: `psql "$DATABASE_URL"`
3. Check RDS security group allows EC2
4. Verify RDS is running in AWS Console

**If Nginx issues:**

1. Test config: `sudo nginx -t`
2. Check logs: `sudo tail -f /var/log/nginx/error.log`
3. Restart: `sudo systemctl restart nginx`

---

## 💡 Monitoring Best Practices

**Daily:**
- Check health endpoint: `curl http://43.204.234.177/health`
- Review error logs: `sudo journalctl -u bloodbank -p err -n 20`

**Weekly:**
- Check disk space: `df -h`
- Review database size
- Check for security updates: `sudo yum check-update`

**Monthly:**
- Review CloudWatch metrics
- Optimize database queries
- Update dependencies

---

## 🚨 Emergency Commands

**If backend is completely down:**

```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@43.204.234.177

# Check what's wrong
sudo systemctl status bloodbank
sudo journalctl -u bloodbank -n 100

# Try to restart
sudo systemctl restart bloodbank

# If that fails, check the app manually
cd /home/ec2-user/bloodbank/backend
source venv/bin/activate
python app.py

# This will show you the exact error
```

**If database is unreachable:**

```bash
# Check RDS status in AWS Console
# Check security groups
# Try connecting manually:
psql "postgresql://dbadmin:PASSWORD@RDS_ENDPOINT:5432/bloodbank"
```

---

**Save these commands for quick reference!** 📌
