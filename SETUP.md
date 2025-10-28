# SmartPath Academy - Setup Guide

## Quick Start (Docker - Recommended)

### 1. Prerequisites
Ensure you have installed:
- Docker Desktop (https://www.docker.com/products/docker-desktop/)
- Git (optional, for version control)

### 2. Initial Setup

**Step 1: Navigate to project directory**
```powershell
cd c:\Users\bouda\Desktop\DJANGOOO
```

**Step 2: Start the application**
```powershell
# Option A: Using the start script
.\start.ps1

# Option B: Manual start
docker-compose up --build -d
```

**Step 3: Wait for services to start** (about 30 seconds)

**Step 4: Create a superuser account**
```powershell
docker-compose exec web python manage.py createsuperuser
```
Follow the prompts to create your admin account.

**Step 5: Access the application**
- **Admin Panel**: http://localhost:8000/admin
- **API Root**: http://localhost:8000/
- **Swagger Docs**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

### 3. Common Commands

**View logs**
```powershell
docker-compose logs -f web
```

**Stop services**
```powershell
docker-compose down
```

**Restart services**
```powershell
docker-compose restart
```

**Run migrations**
```powershell
docker-compose exec web python manage.py migrate
```

**Create migrations**
```powershell
docker-compose exec web python manage.py makemigrations
```

**Access Django shell**
```powershell
docker-compose exec web python manage.py shell
```

**Run tests**
```powershell
docker-compose exec web pytest
```

---

## Local Development (Without Docker)

### 1. Prerequisites
- Python 3.11+
- PostgreSQL 15
- Redis

### 2. Setup Steps

**Step 1: Create virtual environment**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Step 2: Install dependencies**
```powershell
pip install -r requirements.txt
```

**Step 3: Configure environment**
```powershell
copy .env.example .env
```

Edit `.env` and update `DATABASE_URL` to your local PostgreSQL:
```
DATABASE_URL=postgres://your_user:your_password@localhost:5432/smartpathdb
```

**Step 4: Create database**
```sql
CREATE DATABASE smartpathdb;
```

**Step 5: Run migrations**
```powershell
python manage.py migrate
```

**Step 6: Create superuser**
```powershell
python manage.py createsuperuser
```

**Step 7: Start development server**
```powershell
python manage.py runserver
```

**Step 8: Start Celery worker (new terminal)**
```powershell
celery -A SmartPathAcademy worker -l info
```

---

## Project Structure Overview

```
SmartPathAcademy/
├── SmartPathAcademy/          # Main project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py               # URL routing
│   ├── celery.py             # Celery config
│   └── wsgi.py/asgi.py       # Server configs
│
├── accounts/                  # User management app
│   ├── models.py             # User and Profile models
│   ├── views.py              # API views
│   ├── serializers.py        # DRF serializers
│   └── urls.py               # App URLs
│
├── courses/                   # Course management app
│   ├── models.py             # Course, Module, Lesson models
│   └── ...
│
├── gamification/              # Gamification features
│   ├── models.py             # Badge, Level, Points models
│   └── ...
│
├── ai_coach/                  # AI chatbot integration
│   ├── models.py             # Chat sessions, messages
│   └── ...
│
├── analytics/                 # Progress tracking
│   ├── models.py             # Analytics models
│   └── ...
│
├── static/                    # Static files (CSS, JS, images)
├── media/                     # User uploads
├── templates/                 # HTML templates
│
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker services config
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                 # Documentation
```

---

## Environment Variables

Key variables in `.env`:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-secret-key-here` |
| `DEBUG` | Debug mode | `True` or `False` |
| `ALLOWED_HOSTS` | Allowed host names | `localhost,127.0.0.1` |
| `DATABASE_URL` | PostgreSQL connection | `postgres://user:pass@host:port/db` |
| `REDIS_URL` | Redis connection | `redis://redis:6379/0` |
| `GROQ_API_KEY` | Groq API key for AI | `gsk_xxxxx` |
| `CORS_ALLOWED_ORIGINS` | CORS origins | `http://localhost:3000` |

---

## Testing the Application

### 1. Using the Admin Panel

1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Create sample data:
   - Create courses
   - Add modules and lessons
   - Create badges and levels

### 2. Using the API

**Test with Swagger UI:**
1. Visit http://localhost:8000/swagger/
2. Explore available endpoints
3. Try out API calls

**Test with curl/Postman:**
```bash
# Register a user
curl -X POST http://localhost:8000/api/accounts/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123", "password_confirm": "testpass123"}'

# Login (get token)
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# Get user profile (use token from login)
curl -X GET http://localhost:8000/api/accounts/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Troubleshooting

### Docker Issues

**Services won't start:**
```powershell
# Check logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose up --build
```

**Database connection errors:**
```powershell
# Reset database volume
docker-compose down -v
docker-compose up --build
```

**Port already in use:**
- Change port in `docker-compose.yml` from `8000:8000` to `8001:8000`

### Python/Django Issues

**Import errors:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Migration errors:**
```powershell
# Reset migrations (WARNING: loses data)
python manage.py migrate --fake app_name zero
python manage.py migrate app_name
```

---

## Next Steps

1. **Customize Settings**: Update `settings.py` for your needs
2. **Add Sample Data**: Create courses, users, badges
3. **Configure AI**: Ensure GROQ_API_KEY is valid
4. **Test Features**: Try each app's functionality
5. **Deploy**: Follow deployment guide for production

---

## Support

- **Documentation**: See README.md
- **API Docs**: http://localhost:8000/swagger/
- **Issues**: Create GitHub issue
- **Email**: contact@smartpathacademy.com

---

Happy Learning! 🎓
