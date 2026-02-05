# Quick Fix Guide - Registration Failure

## Problem Identified
Your frontend was trying to connect to `https://43.204.234.177/api` but your EC2 backend only supports HTTP (no SSL certificate).

## Solution Applied
Changed `.env.production` from:
```
VITE_API_URL=https://43.204.234.177/api  ❌
```

To:
```
VITE_API_URL=http://43.204.234.177/api  ✅
```

## Next Steps

### 1. Rebuild Frontend
```powershell
cd "C:\Users\Shiwa\OneDrive\Desktop\Blood Bank Anant\frontend"
npm run build
```

### 2. Upload to S3
```powershell
aws s3 sync dist/ s3://bloodbank-frontend/ --delete
```

### 3. Invalidate CloudFront Cache
```powershell
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

**OR** via AWS Console:
1. Go to CloudFront → Your Distribution
2. Click "Invalidations" tab
3. Create invalidation for `/*`
4. Wait 1-2 minutes

### 4. Test Again
Open your CloudFront URL and try registration again!

---

## Alternative: Setup HTTPS on Backend (Recommended for Production)

If you want to use HTTPS properly:

1. Get a domain name
2. Install SSL certificate on EC2 using Let's Encrypt
3. Configure Nginx for HTTPS
4. Update frontend to use `https://yourdomain.com/api`

For now, using HTTP is fine for testing and demonstration purposes.
