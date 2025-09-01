# 🚀 Quick Start Guide

Get your Habit Loop API up and running in minutes!

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Git

## ⚡ Quick Setup

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/habit-loop.git
cd habit-loop
```

### 2. Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r ../requirements.txt
export PYTHONPATH=.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

### 4. Access Your App
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🚀 Deploy to Production

### Option 1: One-Click Deploy
```bash
./deploy.sh
```

### Option 2: Manual Deploy
1. Push to GitHub
2. Go to [render.com](https://render.com)
3. Connect GitHub repo
4. Deploy with:
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🎯 Test Your API

```bash
# Health check
curl http://localhost:8000/health

# Get habits
curl http://localhost:8000/habits

# Create a habit
curl -X POST http://localhost:8000/habits \
  -H "Content-Type: application/json" \
  -d '{"title": "Drink Water", "goal_type": "daily", "schedule_json": {"days": [1,2,3,4,5,6,7]}}'
```

## 🔧 Troubleshooting

**Backend won't start?**
- Check Python version: `python --version`
- Ensure virtual environment is activated
- Set PYTHONPATH: `export PYTHONPATH=.`

**Frontend won't load?**
- Check Node version: `node --version`
- Clear cache: `rm -rf node_modules && npm install`
- Check if backend is running on port 8000

**API calls failing?**
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS settings in backend config
- Ensure frontend is pointing to correct API URL

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [API documentation](http://localhost:8000/docs)
- Check out the ML features in the insights endpoints
- Customize the frontend components

Happy coding! 🎉
