# GitHub Repository Setup Guide

Follow these steps to create a GitHub repository and push your Blood Bank application code.

---

## Step 1: Create GitHub Repository

### 1.1 Go to GitHub
1. Open your browser and go to [https://github.com](https://github.com)
2. Log in to your GitHub account (or create one if you don't have it)

### 1.2 Create New Repository
1. Click the **"+"** icon in the top right corner
2. Select **"New repository"**

### 1.3 Configure Repository
- **Repository name**: `blood-bank-management` (or your preferred name)
- **Description**: `AWS-based Blood Donation Management System with React and Flask`
- **Visibility**: Choose **Public** or **Private**
- **DO NOT** initialize with README, .gitignore, or license (we already have these)
- Click **"Create repository"**

### 1.4 Copy Repository URL
After creation, you'll see a page with setup instructions. Copy the repository URL:
- HTTPS: `https://github.com/YOUR_USERNAME/blood-bank-management.git`
- SSH: `git@github.com:YOUR_USERNAME/blood-bank-management.git`

---

## Step 2: Initialize Git and Push Code

### 2.1 Open Terminal/PowerShell
Open PowerShell in your project directory:
```powershell
cd "C:\Users\Shiwa\OneDrive\Desktop\Blood Bank Anant"
```

### 2.2 Initialize Git Repository
```powershell
git init
```

### 2.3 Configure Git (if first time)
```powershell
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2.4 Add All Files
```powershell
git add .
```

### 2.5 Create Initial Commit
```powershell
git commit -m "Initial commit: Blood Bank Management System with AWS deployment"
```

### 2.6 Add Remote Repository
Replace `YOUR_USERNAME` with your GitHub username:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/blood-bank-management.git
```

### 2.7 Push to GitHub
```powershell
# For first push
git push -u origin main
```

If you get an error about branch name, try:
```powershell
git branch -M main
git push -u origin main
```

---

## Step 3: Verify on GitHub

1. Go to your repository URL: `https://github.com/YOUR_USERNAME/blood-bank-management`
2. You should see all your files uploaded
3. Verify these key files are present:
   - ✅ `README.md`
   - ✅ `DEPLOYMENT.md`
   - ✅ `backend/` folder
   - ✅ `frontend/` folder
   - ✅ `.gitignore`

---

## Step 4: Clone on AWS EC2

Once your code is on GitHub, you can clone it on your EC2 instance:

```bash
# On EC2 instance
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/blood-bank-management.git bloodbank

# Navigate to backend
cd bloodbank/backend

# Continue with deployment steps from DEPLOYMENT.md
```

---

## Common Git Commands for Future Updates

### Update Code on GitHub
```powershell
# After making changes
git add .
git commit -m "Description of changes"
git push
```

### Pull Latest Changes on EC2
```bash
# On EC2 instance
cd /home/ubuntu/bloodbank
git pull origin main

# Restart application
sudo systemctl restart bloodbank
```

### Check Status
```powershell
git status
```

### View Commit History
```powershell
git log --oneline
```

### Create a New Branch
```powershell
git checkout -b feature-name
git push -u origin feature-name
```

---

## Troubleshooting

### Authentication Issues

**Option 1: HTTPS with Personal Access Token (Recommended)**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (full control)
4. Copy the token
5. When pushing, use token as password

**Option 2: SSH Key**
```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

Then use SSH URL:
```powershell
git remote set-url origin git@github.com:YOUR_USERNAME/blood-bank-management.git
```

### Large Files Warning
If you get warnings about large files:
```powershell
# Remove node_modules if accidentally added
git rm -r --cached frontend/node_modules
git commit -m "Remove node_modules"
```

### Wrong Branch Name
If your default branch is `master` instead of `main`:
```powershell
git branch -M main
git push -u origin main
```

---

## Security Best Practices

✅ **Never commit sensitive data:**
- `.env` files with real credentials
- SSH keys (`.pem` files)
- Database passwords
- API keys

✅ **Use .gitignore:**
- Already configured in your project
- Prevents accidental commits of sensitive files

✅ **Use environment variables:**
- Keep `.env.example` with dummy values
- Add real values only on deployment

---

## Quick Reference

```powershell
# Initial setup (one time)
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

# Regular workflow
git add .
git commit -m "Your message"
git push

# Pull updates
git pull

# Check status
git status
```

---

## Next Steps After Pushing to GitHub

1. ✅ Verify all files are on GitHub
2. ✅ Update `DEPLOYMENT.md` with your repository URL
3. ✅ Clone on EC2 instance
4. ✅ Follow deployment steps
5. ✅ Setup CI/CD (optional, for automated deployments)

---

**You're ready to push to GitHub!** 🚀

Follow the commands in Step 2, and your code will be on GitHub for easy deployment to AWS.
