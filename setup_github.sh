#!/bin/bash
# Quick GitHub Setup Script
# Run this to complete GitHub setup after creating repository

echo "=========================================="
echo "Blood Bank - GitHub Setup"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
fi

# Check git config
echo "Checking Git configuration..."
GIT_NAME=$(git config user.name)
GIT_EMAIL=$(git config user.email)

if [ -z "$GIT_NAME" ] || [ -z "$GIT_EMAIL" ]; then
    echo ""
    echo "⚠️  Git user not configured. Please run:"
    echo "   git config --global user.name \"Your Name\""
    echo "   git config --global user.email \"your.email@example.com\""
    echo ""
    exit 1
fi

echo "✅ Git configured as: $GIT_NAME <$GIT_EMAIL>"
echo ""

# Add all files
echo "📦 Adding all files..."
git add .

# Show status
echo ""
echo "📋 Files to be committed:"
git status --short

echo ""
echo "📊 Summary:"
git diff --cached --stat

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Create a GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Name: blood-bank-management"
echo "   - Don't initialize with README"
echo ""
echo "2. Run these commands (replace YOUR_USERNAME):"
echo ""
echo "   git commit -m \"Initial commit: Blood Bank Management System\""
echo "   git branch -M main"
echo "   git remote add origin https://github.com/YOUR_USERNAME/blood-bank-management.git"
echo "   git push -u origin main"
echo ""
echo "3. On AWS EC2, clone with:"
echo "   git clone https://github.com/YOUR_USERNAME/blood-bank-management.git bloodbank"
echo ""
echo "=========================================="
