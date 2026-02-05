# HTTPS Setup Guide for Backend

## Current Issue
Your CloudFront frontend uses HTTPS, but your EC2 backend only supports HTTP, causing "Mixed Content" errors in browsers.

## Solution: Setup HTTPS on EC2 Backend

### Prerequisites
- A domain name (e.g., bloodbridge.com)
- Domain DNS configured to point to your EC2 IP

### Step 1: Install Certbot on EC2

```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@43.204.234.177

# Install Certbot
sudo yum install -y certbot python3-certbot-nginx

# Verify installation
certbot --version
```

### Step 2: Update Nginx Configuration

```bash
# Edit nginx config
sudo nano /etc/nginx/conf.d/bloodbank.conf

# Change server_name from IP to your domain:
# server_name bloodbridge.yourdomain.com;
```

### Step 3: Get SSL Certificate

```bash
# Get certificate (replace with your domain)
sudo certbot --nginx -d bloodbridge.yourdomain.com

# Follow the prompts:
# - Enter email address
# - Agree to terms
# - Choose to redirect HTTP to HTTPS (option 2)
```

### Step 4: Auto-Renewal Setup

```bash
# Test auto-renewal
sudo certbot renew --dry-run

# Certbot automatically sets up auto-renewal via cron
```

### Step 5: Update Frontend API URL

```bash
# Update .env.production
VITE_API_URL=https://bloodbridge.yourdomain.com/api

# Rebuild and redeploy frontend
npm run build
aws s3 sync dist/ s3://bloodbank-frontend/ --delete
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

### Step 6: Update Backend CORS

```bash
# SSH into EC2
cd /home/ec2-user/bloodbank/backend
nano .env

# Update CORS_ORIGIN
CORS_ORIGIN=https://dtjmenu7qik2z.cloudfront.net

# Restart backend
sudo systemctl restart bloodbank
```

---

## Alternative: Use HTTP for Testing

For testing/demo purposes, you can use HTTP for both:

1. Access CloudFront via HTTP: `http://dtjmenu7qik2z.cloudfront.net/`
2. Backend stays on HTTP: `http://43.204.234.177/api`

This works but is not recommended for production due to security concerns.

---

## Cost of Domain + SSL

- **Domain**: $10-15/year (from Namecheap, GoDaddy, etc.)
- **SSL Certificate**: FREE (Let's Encrypt via Certbot)

---

## Quick Test Without Domain

If you don't have a domain yet, test using HTTP CloudFront URL:
```
http://dtjmenu7qik2z.cloudfront.net/
```

This bypasses the mixed content issue and lets you test the application immediately.
