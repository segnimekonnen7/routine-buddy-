#!/bin/bash

# Habit Loop Deployment Script
# This script helps you deploy your FastAPI project to GitHub and Render

echo "🚀 Habit Loop Deployment Setup"
echo "================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📁 Adding files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Initial commit - Habit Loop API with ML features"

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Please add your GitHub repository URL:"
    echo "   git remote add origin https://github.com/yourusername/habit-loop.git"
    echo "   git push -u origin main"
else
    echo "✅ Remote origin already configured"
    echo "🚀 Pushing to GitHub..."
    git push -u origin main
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Go to https://render.com and sign up"
echo "2. Connect your GitHub account"
echo "3. Create new Web Service"
echo "4. Select your habit-loop repository"
echo "5. Use these settings:"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "6. Deploy!"
echo ""
echo "Your API will be available at: https://your-app-name.onrender.com"
echo "API Documentation: https://your-app-name.onrender.com/docs"
