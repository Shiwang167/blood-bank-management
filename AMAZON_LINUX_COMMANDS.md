# Amazon Linux Quick Commands

## Initial Setup (One-Time)

```bash
# 1. Connect to EC2
ssh -i your-key.pem ec2-user@your-ec2-public-ip

# 2. Update system
sudo yum update -y

# 3. Install dependencies
sudo yum install -y python3.11 python3.11-pip python3.11-devel nginx git postgresql15 gcc

# 4. Clone repository
cd /home/ec2-user
git clone https://github.com/YOUR_USERNAME/blood-bank-management.git bloodbank

# 5. Setup Python environment
cd bloodbank/backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 6. Configure environment
cp .env.example .env
nano .env
# Add your DATABASE_URL and settings, then save (Ctrl+X, Y, Enter)

# 7. Create log directories
sudo mkdir -p /var/log/bloodbank /var/run/bloodbank
sudo chown -R ec2-user:ec2-user /var/log/bloodbank /var/run/bloodbank

# 8. Run database migrations
python scripts/migrate_db.py

# 9. Setup systemd service
sudo cp deploy/bloodbank_amazon_linux.service /etc/systemd/system/bloodbank.service
sudo systemctl daemon-reload
sudo systemctl enable bloodbank
sudo systemctl start bloodbank

# 10. Setup Nginx
# Edit nginx.conf to add your EC2 IP
nano deploy/nginx.conf
# Change server_name to your EC2 public IP

sudo cp deploy/nginx.conf /etc/nginx/conf.d/bloodbank.conf
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl start nginx

# 11. Verify
curl http://localhost/health
```

---

## Common Commands

### Application Management
```bash
# View logs
sudo journalctl -u bloodbank -f

# Restart app
sudo systemctl restart bloodbank

# Check status
sudo systemctl status bloodbank
```

### Nginx Management
```bash
# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# View logs
sudo tail -f /var/log/nginx/error.log
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

### Updates
```bash
# Pull latest code
cd /home/ec2-user/bloodbank
git pull origin main

# Update dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Restart
sudo systemctl restart bloodbank
```

---

## Key Differences from Ubuntu

| Command | Ubuntu | Amazon Linux |
|---------|--------|--------------|
| Update | `sudo apt-get update` | `sudo yum update -y` |
| Install | `sudo apt-get install` | `sudo yum install` |
| User | `ubuntu` | `ec2-user` |
| Python | `python3.11` | `python3.11` |
| PostgreSQL | `postgresql-client` | `postgresql15` |

---

## Troubleshooting

**App won't start:**
```bash
sudo journalctl -u bloodbank -n 50
```

**Can't connect to database:**
```bash
psql "$DATABASE_URL"
# Check RDS security group allows EC2
```

**Nginx errors:**
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

---

## Environment Variables (.env)

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
PORT=5000
JWT_SECRET=your-jwt-secret-here
DATABASE_URL=postgresql://dbadmin:password@rds-endpoint.rds.amazonaws.com:5432/bloodbank
CORS_ORIGIN=http://your-ec2-public-ip
DONATION_INTERVAL_DAYS=90
LOW_STOCK_THRESHOLD=5
CRITICAL_STOCK_THRESHOLD=3
```

---

**Full guide:** See DEPLOYMENT_AMAZON_LINUX.md
