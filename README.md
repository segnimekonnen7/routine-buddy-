# 🚀 Habit Loop - Science-Backed Habit Builder

A full-stack habit tracking application with ML-powered insights and adaptive reminders.

## 🌐 Live Demo

**👉 [Try Habit Loop Now](https://segnimekonnen7.github.io/routine-buddy-/)**

## ✨ Features

- **Smart Habit Tracking** - Track daily habits with flexible scheduling
- **ML-Powered Insights** - Get personalized recommendations and success predictions  
- **Adaptive Reminders** - Optimal reminder timing based on your completion patterns
- **Progress Analytics** - Visualize your habit streaks and consistency
- **Modern UI** - Clean, responsive interface built with modern web technologies

## 🏗️ Architecture

- **Frontend**: HTML5 + Tailwind CSS + Vanilla JavaScript
- **Backend**: FastAPI with Python (deployed on Render)
- **Database**: In-memory storage with demo data
- **Deployment**: GitHub Pages + Render

## 🚀 Quick Start

1. **Use the Live App**: Visit [https://segnimekonnen7.github.io/routine-buddy-/](https://segnimekonnen7.github.io/routine-buddy-/)

2. **Local Development**:
   ```bash
   # Clone the repository
   git clone https://github.com/segnimekonnen7/routine-buddy-.git
   cd routine-buddy-
   
   # Open the app
   open index.html
   ```

## 📱 How to Use

1. **View Habits** - See your current habits and streaks
2. **Check In** - Mark habits as completed for the day
3. **Create Habits** - Add new habits to track
4. **Track Progress** - Monitor your consistency and streaks

## 🔧 API Endpoints

The app connects to a live API at `https://routine-h9ig.onrender.com`:

- `GET /habits` - Get all habits
- `POST /habits` - Create new habit
- `POST /habits/{id}/checkin` - Check in a habit
- `POST /habits/{id}/miss` - Mark habit as missed

## 🎯 Demo Data

The app comes with sample habits:
- **Drink Water** - Stay hydrated (5-day streak)
- **Exercise** - 30 minutes daily (3-day streak)  
- **Read** - Personal development (2-day streak)

## 🛠️ Development

### Frontend
- Pure HTML5 + CSS + JavaScript
- Tailwind CSS for styling
- Axios for API calls
- Responsive design

### Backend
- FastAPI with Python
- CORS enabled for web access
- In-memory data storage
- Deployed on Render

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Built with ❤️ using modern web technologies**