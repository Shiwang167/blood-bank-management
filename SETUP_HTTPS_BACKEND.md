# How to Setup HTTPS on Your Backend (EC2)

## 🎯 Goal
Make your backend API accessible via HTTPS so your CloudFront HTTPS frontend can communicate with it.

---

## ⚠️ **Important: You Need a Domain Name**

**You CANNOT get a free SSL certificate for an IP address.** You need a domain name like:
- `bloodbridge.com`
- `api.yourname.com`
- etc.

**Cost:** ~$10-15/year from registrars like:
- Namecheap.com
- GoDaddy.com
- Google Domains
- AWS Route 53

---

## 📋 **Two Options:**

### **Option 1: Get a Domain and Setup HTTPS (Proper Solution)**
### **Option 2: Use HTTP for Testing (Quick Workaround)**

---

## 🚀 **Option 1: Setup HTTPS with Domain (Recommended)**

### **Step 1: Get a Domain Name**

1. Go to Namecheap.com or GoDaddy.com
2. Search for available domain (e.g., `bloodbridge-yourname.com`)
3. Purchase domain (~$10-15/year)
4. Wait for domain activation (usually instant)

---

### **Step 2: Point Domain to Your EC2**

**Using Route 53 (AWS):**

1. Go to **AWS Route 53 Console**
2. Click **"Create hosted zone"**
3. Enter your domain name
4. Click **"Create hosted zone"**
5. Click **"Create record"**
6. Configure:
   - Record name: `api` (or leave blank for root domain)
   - Record type: `A`
   - Value: `43.204.234.177` (your EC2 IP)
   - TTL: `300`
7. Click **"Create records"**
8. Copy the **NS (nameserver) records**
9. Go to your domain registrar (Namecheap/GoDaddy)
10. Update nameservers to the Route 53 NS records

**Wait 10-60 minutes for DNS propagation.**

---

### **Step 3: Install SSL Certificate on EC2**

SSH into your EC2 instance:

```bash
ssh -i your-key.pem ec2-user@43.204.234.177
```

**Install Certbot:**

```bash
# Install Certbot for Amazon Linux
sudo yum install -y certbot python3-certbot-nginx

# Verify installation
certbot --version
```

---

### **Step 4: Update Nginx Configuration**

```bash
# Edit Nginx config
sudo nano /etc/nginx/conf.d/bloodbank.conf
```

**Change the `server_name` line from IP to your domain:**

```nginx
# Before:
server_name 43.204.234.177;

# After (replace with your actual domain):
server_name api.bloodbridge.com;
```

**Save:** `Ctrl+X`, `Y`, `Enter`

**Test Nginx config:**
```bash
sudo nginx -t
```

**Reload Nginx:**
```bash
sudo systemctl reload nginx
```

---

### **Step 5: Get SSL Certificate**

```bash
# Get certificate (replace with your domain)
sudo certbot --nginx -d api.bloodbridge.com

# Follow the prompts:
# 1. Enter your email address
# 2. Agree to Terms of Service (Y)
# 3. Share email with EFF (optional - Y or N)
# 4. Choose to redirect HTTP to HTTPS (option 2)
```

**Certbot will:**
- Verify domain ownership
- Generate SSL certificate
- Automatically configure Nginx for HTTPS
- Setup auto-renewal

**Test auto-renewal:**
```bash
sudo certbot renew --dry-run
```

---

### **Step 6: Update Backend CORS**

```bash
cd /home/ec2-user/bloodbank/backend
nano .env
```

**Update CORS_ORIGIN:**
```bash
CORS_ORIGIN=https://dtjmenu7qik2z.cloudfront.net
```

**Save and restart:**
```bash
sudo systemctl restart bloodbank
sudo systemctl status bloodbank
```

---

### **Step 7: Update Frontend API URL**

On your **local machine:**

```bash
cd "C:\Users\Shiwa\OneDrive\Desktop\Blood Bank Anant\frontend"
```

**Edit `.env.production`:**
```bash
VITE_API_URL=https://api.bloodbridge.com/api
```

**Rebuild and deploy:**
```powershell
npm run build
aws s3 sync dist/ s3://bloodbank-frontend/ --delete
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

---

### **Step 8: Test**

1. Wait 2-3 minutes for CloudFront invalidation
2. Open: `https://dtjmenu7qik2z.cloudfront.net/`
3. Try registration
4. **It should work!** ✅

---

## 🔧 **Option 2: Quick Workaround (No Domain Needed)**

If you don't want to buy a domain right now, you can test using HTTP:

### **A. Update CloudFront to Allow HTTP**

1. Go to **CloudFront Console**
2. Click your distribution
3. Click **"Behaviors"** tab
4. Select the default behavior
5. Click **"Edit"**
6. Change **"Viewer protocol policy"** to: `HTTP and HTTPS`
7. Click **"Save changes"**
8. Wait 5-10 minutes for deployment

### **B. Access via HTTP**

Try accessing: `http://dtjmenu7qik2z.cloudfront.net/`

If it still redirects to HTTPS, use the **S3 website endpoint** instead.

---

### **C. Find S3 Website Endpoint**

1. Go to **S3 Console**
2. Click `bloodbank-frontend` bucket
3. Go to **Properties** tab
4. Scroll to **"Static website hosting"**
5. Copy the **Bucket website endpoint**
   - Example: `http://bloodbank-frontend.s3-website-ap-south-1.amazonaws.com`

**Open that URL** - it will be HTTP and work with your HTTP backend!

---

## 📊 **Comparison:**

| Solution | Cost | Time | Production Ready |
|----------|------|------|------------------|
| **HTTPS with Domain** | $10-15/year | 1-2 hours | ✅ Yes |
| **HTTP S3 Endpoint** | Free | 5 minutes | ❌ No (not secure) |

---

## 🎯 **Recommended Approach:**

**For Testing/Demo:**
- Use S3 HTTP endpoint now
- Test all features
- Verify everything works

**For Production/Portfolio:**
- Get a domain ($10-15)
- Setup HTTPS on backend
- Use CloudFront HTTPS
- Professional and secure! ✅

---

## 💡 **Quick Commands Summary:**

### **If You Have a Domain:**

```bash
# On EC2
sudo yum install -y certbot python3-certbot-nginx
sudo nano /etc/nginx/conf.d/bloodbank.conf  # Update server_name
sudo certbot --nginx -d api.yourdomain.com
sudo systemctl restart bloodbank

# On Local Machine
# Update .env.production with HTTPS URL
npm run build
aws s3 sync dist/ s3://bloodbank-frontend/ --delete
```

### **If No Domain (Quick Test):**

1. Go to S3 Console
2. Find bucket website endpoint
3. Open that HTTP URL
4. Test your app!

---

## ❓ **Which Option Do You Want?**

1. **Buy a domain and setup HTTPS properly** (recommended for portfolio)
2. **Use S3 HTTP endpoint for quick testing** (works immediately)

Let me know and I'll guide you through the specific steps!
