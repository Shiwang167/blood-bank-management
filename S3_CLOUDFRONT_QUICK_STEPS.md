# S3 + CloudFront Quick Steps

## 🚀 Fast Deployment Guide

### Part 1: Build Frontend (Local Machine)

```powershell
# 1. Navigate to frontend
cd "C:\Users\Shiwa\OneDrive\Desktop\Blood Bank Anant\frontend"

# 2. Update .env.production
# VITE_API_URL=http://YOUR_EC2_PUBLIC_IP/api

# 3. Install and build
npm install
npm run build
```

---

### Part 2: Create S3 Bucket

**AWS Console → S3 → Create bucket:**

1. **Bucket name:** `bloodbank-frontend` (must be unique)
2. **Region:** Same as EC2 (e.g., `ap-south-1`)
3. **Uncheck** "Block all public access" ⚠️
4. Click **Create bucket**

**Enable Static Website Hosting:**
- Properties → Static website hosting → Edit
- Enable
- Index: `index.html`
- Error: `index.html`
- Save

**Add Bucket Policy:**
- Permissions → Bucket policy → Edit
- Paste (replace bucket name):

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::bloodbank-frontend/*"
  }]
}
```

---

### Part 3: Upload Files

**Upload all files from `dist` folder to S3 bucket**

Using Console:
- Click Upload
- Add all files from `dist` folder
- Upload

Using AWS CLI:
```powershell
aws s3 sync dist/ s3://bloodbank-frontend/ --delete
```

**Test:** Open S3 website endpoint

---

### Part 4: Create CloudFront Distribution

**AWS Console → CloudFront → Create distribution:**

1. **Origin domain:** Type manually (don't use dropdown):
   ```
   bloodbank-frontend.s3-website.ap-south-1.amazonaws.com
   ```

2. **Viewer protocol:** Redirect HTTP to HTTPS

3. **Default root object:** `index.html`

4. Click **Create distribution**

5. Wait 5-15 minutes for deployment

---

### Part 5: Configure Error Pages

**CloudFront → Your distribution → Error pages:**

Create two custom error responses:

**403 Error:**
- HTTP error code: 403
- Response page path: `/index.html`
- HTTP response code: 200

**404 Error:**
- HTTP error code: 404
- Response page path: `/index.html`
- HTTP response code: 200

---

### Part 6: Update Backend CORS

**On EC2:**

```bash
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

cd /home/ec2-user/bloodbank/backend
nano .env

# Update CORS_ORIGIN with CloudFront domain:
# CORS_ORIGIN=https://d1234567890abc.cloudfront.net

# Save and restart
sudo systemctl restart bloodbank
```

---

### Part 7: Test

Open CloudFront URL:
```
https://d1234567890abc.cloudfront.net
```

✅ Your app is live!

---

## 🔄 Update Frontend

```powershell
# Rebuild
npm run build

# Upload
aws s3 sync dist/ s3://bloodbank-frontend/ --delete

# Invalidate cache
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

---

## 💰 Cost

- S3: ~$1-2/month
- CloudFront: ~$1-5/month
- **Total: ~$2-7/month**

---

## 🎯 URLs

- **S3 Website:** `http://BUCKET.s3-website.REGION.amazonaws.com`
- **CloudFront:** `https://DISTRIBUTION_ID.cloudfront.net`
- **Backend API:** `http://EC2_PUBLIC_IP/api`

---

**Full guide:** See FRONTEND_S3_CLOUDFRONT.md
