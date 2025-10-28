# 🎓 SmartPath Academy

An intelligent e-learning platform built with Django 4.2, featuring AI-powered learning assistance, gamification, and personalized learning paths.

## ✨ Features

- **📚 Course Management**: Browse, enroll, and track progress in programming courses
- **🤖 AI Learning Coach**: Groq-powered chatbot for instant learning assistance
- **🎮 Gamification**: Badges, achievements, XP points, and leaderboards
- **📊 Analytics Dashboard**: Track learning progress with visual charts
- **🎯 Personalized Learning**: Learning style assessment and customized course recommendations
- **🔐 Secure Authentication**: Custom user authentication with multi-step registration
- **📱 Responsive Design**: Beautiful WowDash admin template integration
- **⚡ Real-time Updates**: Redis caching and Celery background tasks

## 🛠️ Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL 15
- **Cache & Queue**: Redis, Celery
- **Frontend**: Bootstrap 5, WowDash Template
- **AI**: Groq API
- **Deployment**: Docker, Docker Compose

## 📦 Project Structure

```
SmartPathAcademy/
├── accounts/          # User authentication & profiles
├── courses/           # Course management & content
├── gamification/      # Badges, achievements, XP system
├── ai_coach/          # AI-powered learning assistant
├── analytics/         # Progress tracking & analytics
├── static/            # CSS, JS, images
├── templates/         # HTML templates
├── media/             # User uploads
└── docker-compose.yml # Docker configuration
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/smartpath-academy.git
   cd smartpath-academy
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=postgres://smartpath:smartpath123@db:5432/smartpathdb
   REDIS_URL=redis://redis:6379/0
   GROQ_API_KEY=your-groq-api-key
   ```

3. **Build and run with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser --noinput
   ```

6. **Load sample data**
   ```bash
   docker-compose exec web python manage.py seed_sample_data
   ```

7. **Access the application**
   - Frontend: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - API Docs: http://localhost:8000/api/swagger/

### Default Credentials

- **Admin**: admin / admin123
- **Sample Students**: Check seed_sample_data command output

## 📚 API Documentation

Visit http://localhost:8000/api/swagger/ for interactive API documentation.

## 🎯 Key Endpoints

- `/accounts/login/` - Student login
- `/accounts/register/` - Student registration with learning style assessment
- `/dashboard/` - Student dashboard
- `/courses/` - Browse available courses
- `/ai-coach/` - AI learning assistant chat
- `/leaderboard/` - Gamification leaderboard

## 🔧 Development

### Run tests
```bash
docker-compose exec web python manage.py test
```

### Collect static files
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Create new migrations
```bash
docker-compose exec web python manage.py makemigrations
```

## 📊 Database Schema

- **User**: Custom user model with roles (ADMIN, INSTRUCTOR, STUDENT)
- **StudentProfile**: Learning preferences, XP, streaks, levels
- **Course**: Title, instructor, category, difficulty, lessons
- **Lesson**: Content types (VIDEO, TEXT, QUIZ, CODING)
- **Quiz**: Questions, answers, scoring
- **Badge**: Achievements with requirements
- **Enrollment**: Student course progress tracking

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- WowDash Admin Template
- Django Community
- Groq AI Platform

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using Django**
