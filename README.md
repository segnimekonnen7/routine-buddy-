# Habit Loop - Science-Backed Habit Builder

A full-stack habit tracking application built with FastAPI backend and Next.js frontend, featuring ML-powered insights and adaptive reminders.

## 🚀 Features

- **Smart Habit Tracking**: Track daily habits with flexible scheduling
- **ML-Powered Insights**: Get personalized recommendations and success predictions
- **Adaptive Reminders**: Optimal reminder timing based on your completion patterns
- **Progress Analytics**: Visualize your habit streaks and consistency
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS

## 🏗️ Architecture

- **Backend**: FastAPI with Python 3.11+
- **Frontend**: Next.js 14 with TypeScript
- **Database**: SQLAlchemy with SQLite (local) / PostgreSQL (production)
- **ML Features**: Pandas/NumPy for data analysis
- **Authentication**: JWT-based with magic link emails

## 📁 Project Structure

```
habit-loop/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── core/           # Configuration and settings
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routers/        # API routes
│   │   └── services/       # Business logic and ML services
│   └── alembic/            # Database migrations
├── frontend/               # Next.js frontend
│   ├── app/               # App Router pages
│   ├── components/        # React components
│   └── lib/              # Utilities and API client
├── main.py               # Deployment entry point
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
└── render.yaml          # Render deployment config
```

## 🛠️ Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd habit-loop/backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   export PYTHONPATH=.
   ```

5. **Start the backend**:
   ```bash
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd habit-loop/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the frontend**:
   ```bash
   npm run dev
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🚀 Deployment

### Option 1: Render (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Habit Loop API"
   git remote add origin https://github.com/yourusername/habit-loop.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [render.com](https://render.com) and sign up
   - Connect your GitHub account
   - Create new Web Service
   - Select your `habit-loop` repository
   - Use these settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Deploy!

### Option 2: Docker

1. **Build the image**:
   ```bash
   docker build -t habit-loop .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 habit-loop
   ```

### Option 3: Railway

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

## 📊 API Endpoints

### Core Endpoints
- `GET /health` - Health check
- `GET /habits` - Get all habits
- `POST /habits` - Create new habit
- `POST /habits/{id}/checkin` - Check in a habit
- `POST /habits/{id}/miss` - Mark habit as missed

### ML-Powered Insights
- `GET /insights/habits/{id}/success-prediction` - Predict habit success
- `GET /insights/habits/{id}/optimal-reminder` - Get optimal reminder time
- `GET /insights/habits/{id}/completion-stats` - Get completion statistics
- `GET /insights/habits/{id}/recommendations` - Get personalized recommendations

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=sqlite:///./habitloop.db

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# JWT
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080

# Email (optional)
SENDGRID_API_KEY=your-sendgrid-key
ALERTS_FROM_EMAIL=alerts@habitloop.local
APP_BASE_URL=http://localhost:3000
```

## 🧪 Testing

Run the test suite:

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📈 ML Features

The application includes several ML-powered features:

1. **Smart Reminder Timing**: Uses ε-greedy algorithm to find optimal reminder times
2. **Success Prediction**: Rule-based prediction using completion rates and streaks
3. **Completion Statistics**: Statistical analysis of habit patterns
4. **Personalized Recommendations**: Data-driven suggestions for habit improvement

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/yourusername/habit-loop/issues) page
2. Create a new issue with detailed information
3. Join our community discussions

## 🎯 Roadmap

- [ ] User authentication and profiles
- [ ] Habit sharing and social features
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Integration with fitness trackers
- [ ] AI-powered habit suggestions

---

Built with ❤️ using FastAPI, Next.js, and modern web technologies.
# Force redeploy - Mon Sep  1 17:59:17 CDT 2025
