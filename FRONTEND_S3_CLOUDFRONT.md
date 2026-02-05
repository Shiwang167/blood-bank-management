# Frontend Deployment - S3 + CloudFront

Complete guide to deploy your React frontend to AWS S3 with CloudFront CDN.

---

## 🎯 Architecture Overview

```
Users → CloudFront (CDN) → S3 Bucket (Static Files)
                ↓
        EC2 Backend API (CORS enabled)
```

**Benefits:**
- ✅ Global CDN distribution (fast worldwide)
- ✅ HTTPS by default
- ✅ Scalable (handles millions of users)
- ✅ Cost-effective (~$1-5/month)
- ✅ Separate frontend/backend deployment

---

## 📋 Prerequisites

- ✅ Backend deployed and running on EC2
- ✅ EC2 public IP noted
- ✅ AWS Console access
- ✅ Node.js installed locally

---

## Part 1: Build the Frontend

### Step 1: Update Environment Configuration

On your **local machine** (Windows):

```powershell
cd "C:\Users\Shiwa\OneDrive\Desktop\Blood Bank Anant\frontend"
```

Edit `.env.production`:

```bash
# Replace with your EC2 public IP
VITE_API_URL=http://YOUR_EC2_PUBLIC_IP/api
```

**Example:**
```bash
VITE_API_URL=http://13.232.45.67/api
```

---

### Step 2: Install Dependencies

```powershell
npm install
```

---

### Step 3: Build for Production

```powershell
npm run build
```

This creates a `dist` folder with optimized static files.

**Verify the build:**
```powershell
dir dist
```

You should see:
- `index.html`
- `assets/` folder with JS and CSS files

---

## Part 2: Create S3 Bucket

### Step 1: Go to S3 Console

1. Open AWS Console
2. Go to **S3** service
3. Click **"Create bucket"**

---

### Step 2: Configure Bucket

**Bucket name:** `bloodbank-frontend` (must be globally unique)
- If taken, try: `bloodbank-app-frontend-2026`

**AWS Region:** Same as your EC2 (e.g., `ap-south-1`)

**Object Ownership:**
- ✅ ACLs disabled (recommended)

**Block Public Access settings:**
- ⚠️ **UNCHECK** "Block all public access"
- ✅ Check the acknowledgment box

**Bucket Versioning:**
- Enable (optional, for rollback capability)

**Tags:** (optional)
- Key: `Project`, Value: `BloodBank`

**Default encryption:**
- Enable (recommended)

Click **"Create bucket"**

---

### Step 3: Enable Static Website Hosting

1. Click on your bucket name
2. Go to **Properties** tab
3. Scroll to **Static website hosting**
4. Click **Edit**

Configure:
```
Static website hosting: Enable
Hosting type: Host a static website
Index document: index.html
Error document: index.html  ← Important for React Router!
```

Click **Save changes**

**Note the endpoint URL** (e.g., `http://bloodbank-frontend.s3-website.ap-south-1.amazonaws.com`)

---

### Step 4: Configure Bucket Policy

1. Go to **Permissions** tab
2. Scroll to **Bucket policy**
3. Click **Edit**

Paste this policy (replace `bloodbank-frontend` with your bucket name):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::bloodbank-frontend/*"
    }
  ]
}
```

Click **Save changes**

---

## Part 3: Upload Frontend Files

### Option A: Using AWS Console (Easiest)

1. Go to your bucket
2. Click **Upload**
3. Click **Add files** and **Add folder**
4. Select ALL files from your `dist` folder:
   - `index.html`
   - `assets/` folder
   - `vite.svg` (if exists)
   - Any other files

5. Click **Upload**

Wait for upload to complete.

---

### Option B: Using AWS CLI (Faster)

**Install AWS CLI** (if not installed):
- Download from: https://aws.amazon.com/cli/

**Configure AWS CLI:**
```powershell
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `ap-south-1`
- Default output format: `json`

**Upload files:**
```powershell
cd "C:\Users\Shiwa\OneDrive\Desktop\Blood Bank Anant\frontend"

aws s3 sync dist/ s3://bloodbank-frontend/ --delete
```

---

### Step 5: Test S3 Website

Open the S3 website endpoint in your browser:
```
http://bloodbank-frontend.s3-website.ap-south-1.amazonaws.com
```

Your app should load! 🎉

---

## Part 4: Setup CloudFront CDN

### Step 1: Create CloudFront Distribution

1. Go to **CloudFront** service
2. Click **Create distribution**

---

### Step 2: Configure Origin

**Origin domain:**
- **DON'T** select the S3 bucket from dropdown
- **MANUALLY TYPE** your S3 website endpoint:
  ```
  bloodbank-frontend.s3-website.ap-south-1.amazonaws.com
  ```
  (Remove `http://` - just the domain)

**Protocol:**
- HTTP only (S3 website endpoints don't support HTTPS)

**Name:** `bloodbank-s3-origin` (auto-filled)

---

### Step 3: Configure Default Cache Behavior

**Viewer protocol policy:**
- ✅ Redirect HTTP to HTTPS

**Allowed HTTP methods:**
- ✅ GET, HEAD, OPTIONS

**Cache policy:**
- CachingOptimized (recommended)

---

### Step 4: Configure Settings

**Price class:**
- Use all edge locations (best performance)
- OR Use only North America and Europe (cheaper)

**Alternate domain name (CNAME):** (optional)
- Leave empty for now (or add your custom domain)

**Custom SSL certificate:**
- Default CloudFront certificate

**Default root object:**
- `index.html`

**Description:** `BloodBank Frontend Distribution`

Click **Create distribution**

---

### Step 5: Wait for Deployment

Status will show **"Deploying"** → **"Enabled"** (5-15 minutes)

**Copy the Distribution domain name:**
```
d1234567890abc.cloudfront.net
```

---

### Step 6: Configure Error Pages (Important for React Router!)

1. Click on your distribution
2. Go to **Error pages** tab
3. Click **Create custom error response**

**Create two error responses:**

**Error Response 1:**
```
HTTP error code: 403
Customize error response: Yes
Response page path: /index.html
HTTP response code: 200
```

**Error Response 2:**
```
HTTP error code: 404
Customize error response: Yes
Response page path: /index.html
HTTP response code: 200
```

This ensures React Router works correctly!

---

## Part 5: Update Backend CORS

Your backend needs to allow requests from CloudFront.

### On EC2:

```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

# Edit .env file
cd /home/ec2-user/bloodbank/backend
nano .env
```

**Update CORS_ORIGIN:**
```bash
# Add your CloudFront domain
CORS_ORIGIN=https://d1234567890abc.cloudfront.net
```

**Save:** `Ctrl+X`, `Y`, `Enter`

**Restart backend:**
```bash
sudo systemctl restart bloodbank
```

---

## Part 6: Test Your Application

### Open CloudFront URL

```
https://d1234567890abc.cloudfront.net
```

Your Blood Bank application should now be live! 🎉

### Test Functionality

1. ✅ Register a new user
2. ✅ Login
3. ✅ Navigate between pages
4. ✅ Create blood requests (if hospital user)
5. ✅ Check API calls work

---

## 🔄 Updating Your Frontend

When you make changes to your frontend:

### Step 1: Rebuild

```powershell
cd "C:\Users\Shiwa\OneDrive\Desktop\Blood Bank Anant\frontend"
npm run build
```

### Step 2: Upload to S3

**Using AWS Console:**
- Delete old files in S3 bucket
- Upload new files from `dist` folder

**Using AWS CLI:**
```powershell
aws s3 sync dist/ s3://bloodbank-frontend/ --delete
```

### Step 3: Invalidate CloudFront Cache

**Using AWS Console:**
1. Go to CloudFront → Your distribution
2. Click **Invalidations** tab
3. Click **Create invalidation**
4. Object paths: `/*`
5. Click **Create invalidation**

**Using AWS CLI:**
```powershell
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

Wait 1-2 minutes for cache to clear.

---

## 💰 Cost Estimation

### S3 Storage
- Storage: ~$0.023 per GB/month
- Requests: ~$0.005 per 1,000 requests
- **Estimated:** $0.50 - $2/month

### CloudFront
- Data transfer: ~$0.085 per GB (first 10 TB)
- Requests: ~$0.0075 per 10,000 requests
- **Estimated:** $1 - $5/month (low traffic)

### Total Frontend Cost
**~$2-7/month** for moderate traffic

---

## 🔒 Security Best Practices

### 1. Enable CloudFront HTTPS Only

Already configured with "Redirect HTTP to HTTPS"

### 2. Add Security Headers

In CloudFront → Behaviors → Edit:

Add response headers policy:
- `Strict-Transport-Security`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `X-XSS-Protection`

### 3. Restrict S3 Bucket Access (Advanced)

Use CloudFront Origin Access Identity (OAI) to prevent direct S3 access.

---

## 🌐 Custom Domain (Optional)

### If You Have a Domain:

1. **Get SSL Certificate:**
   - Go to AWS Certificate Manager (ACM)
   - Request certificate for `bloodbank.yourdomain.com`
   - Validate via DNS or email

2. **Add CNAME to CloudFront:**
   - Edit distribution
   - Add alternate domain name: `bloodbank.yourdomain.com`
   - Select your SSL certificate

3. **Update DNS:**
   - Add CNAME record in your domain registrar:
   - `bloodbank` → `d1234567890abc.cloudfront.net`

---

## 🐛 Troubleshooting

### Frontend Loads But API Calls Fail

**Check:**
1. CORS_ORIGIN in backend `.env` includes CloudFront domain
2. Backend is running: `sudo systemctl status bloodbank`
3. API URL in frontend `.env.production` is correct
4. EC2 security group allows HTTP/HTTPS

**Test API directly:**
```bash
curl http://YOUR_EC2_IP/health
```

### CloudFront Shows Old Content

**Solution:**
- Create invalidation for `/*`
- Wait 1-2 minutes

### React Router Pages Show 404

**Solution:**
- Add custom error responses (403 and 404 → /index.html)
- Already covered in Step 6

### S3 Access Denied

**Check:**
1. Bucket policy allows public read
2. Block public access is disabled
3. Files are uploaded correctly

---

## 📋 Deployment Checklist

- [ ] Frontend built with correct API URL
- [ ] S3 bucket created and configured
- [ ] Static website hosting enabled
- [ ] Bucket policy allows public read
- [ ] Files uploaded to S3
- [ ] S3 website endpoint works
- [ ] CloudFront distribution created
- [ ] Error pages configured (403, 404)
- [ ] CloudFront distribution deployed
- [ ] Backend CORS updated with CloudFront domain
- [ ] Backend restarted
- [ ] Application tested via CloudFront URL
- [ ] All features working

---

## 🎯 Quick Reference

### S3 Bucket URL
```
http://bloodbank-frontend.s3-website.ap-south-1.amazonaws.com
```

### CloudFront URL
```
https://d1234567890abc.cloudfront.net
```

### Update Frontend
```powershell
npm run build
aws s3 sync dist/ s3://bloodbank-frontend/ --delete
aws cloudfront create-invalidation --distribution-id ID --paths "/*"
```

---

## ✅ Summary

**What You've Deployed:**

1. ✅ **Backend:** EC2 + RDS PostgreSQL
2. ✅ **Frontend:** S3 + CloudFront CDN
3. ✅ **Database:** RDS with migrations
4. ✅ **Auto-restart:** Systemd service
5. ✅ **Reverse proxy:** Nginx
6. ✅ **Global CDN:** CloudFront

**Your Blood Bank application is now production-ready!** 🚀

---

## 📞 Need Help?

Common issues:
- **CORS errors:** Update backend CORS_ORIGIN
- **404 on routes:** Configure CloudFront error pages
- **Old content:** Create CloudFront invalidation
- **API not working:** Check EC2 security groups and backend status

**Your application is now live and accessible worldwide!** 🌍
