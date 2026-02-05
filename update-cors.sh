#!/bin/bash
# Quick fix script to update backend CORS for CloudFront HTTPS

echo "=== Updating Backend CORS Configuration ==="
echo ""

# SSH into EC2 and update CORS
cat << 'EOF'
Run these commands on your EC2 instance:

# SSH into EC2
ssh -i your-key.pem ec2-user@43.204.234.177

# Navigate to backend
cd /home/ec2-user/bloodbank/backend

# Backup current .env
cp .env .env.backup

# Update CORS_ORIGIN to allow CloudFront HTTPS
nano .env

# Change this line:
# CORS_ORIGIN=http://localhost:5173

# To this (replace with your CloudFront URL):
# CORS_ORIGIN=https://dtjmenu7qik2z.cloudfront.net

# Save and exit (Ctrl+X, Y, Enter)

# Restart the backend service
sudo systemctl restart bloodbank

# Verify it's running
sudo systemctl status bloodbank

# Check logs
sudo journalctl -u bloodbank -n 20

echo "✅ CORS updated! Try registration again."
EOF
