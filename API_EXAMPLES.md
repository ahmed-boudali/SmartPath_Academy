# API Testing Examples

## Authentication

### Register User
```bash
POST http://localhost:8000/api/accounts/users/register/
Content-Type: application/json

{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Login
```bash
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
    "username": "johndoe",
    "password": "SecurePass123!"
}
```

Response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Get Current User
```bash
GET http://localhost:8000/api/accounts/users/me/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## Courses

### List Courses
```bash
GET http://localhost:8000/api/courses/courses/
```

### Get Course Detail
```bash
GET http://localhost:8000/api/courses/courses/1/
```

### Enroll in Course
```bash
POST http://localhost:8000/api/courses/courses/1/enroll/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### List Modules
```bash
GET http://localhost:8000/api/courses/modules/?course=1
```

### List Lessons
```bash
GET http://localhost:8000/api/courses/lessons/?module=1
```

---

## Gamification

### Get User Points
```bash
GET http://localhost:8000/api/gamification/points/me/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### List Badges
```bash
GET http://localhost:8000/api/gamification/badges/
```

### Get User Badges
```bash
GET http://localhost:8000/api/gamification/user-badges/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Weekly Leaderboard
```bash
GET http://localhost:8000/api/gamification/leaderboard/weekly/
```

### Monthly Leaderboard
```bash
GET http://localhost:8000/api/gamification/leaderboard/monthly/
```

---

## AI Coach

### Create Chat Session
```bash
POST http://localhost:8000/api/ai-coach/sessions/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
    "title": "Learning Python",
    "is_active": true
}
```

### Send Message to AI Coach
```bash
POST http://localhost:8000/api/ai-coach/sessions/1/send_message/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
    "message": "How do I get started with Python programming?"
}
```

### List Chat Sessions
```bash
GET http://localhost:8000/api/ai-coach/sessions/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Create Coaching Goal
```bash
POST http://localhost:8000/api/ai-coach/goals/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
    "title": "Complete Python Basics Course",
    "description": "Finish all modules in Python Basics",
    "target_date": "2025-12-31"
}
```

### Get AI Recommendations
```bash
GET http://localhost:8000/api/ai-coach/recommendations/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## Analytics

### Get Learning Progress
```bash
GET http://localhost:8000/api/analytics/progress/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Get Progress Summary
```bash
GET http://localhost:8000/api/analytics/progress/summary/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Submit Quiz Attempt
```bash
POST http://localhost:8000/api/analytics/quiz-attempts/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
    "lesson": 1,
    "score": 85.5,
    "total_questions": 10,
    "correct_answers": 8,
    "time_taken": 600,
    "answers": {
        "q1": "answer1",
        "q2": "answer2"
    }
}
```

### Get Quiz Statistics
```bash
GET http://localhost:8000/api/analytics/quiz-attempts/statistics/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Get Current Study Streak
```bash
GET http://localhost:8000/api/analytics/streaks/current/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Get Performance Dashboard
```bash
GET http://localhost:8000/api/analytics/metrics/dashboard/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Track User Activity
```bash
POST http://localhost:8000/api/analytics/activities/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
    "activity_type": "lesson_complete",
    "metadata": {
        "lesson_id": 1,
        "course_id": 1,
        "time_spent": 1200
    }
}
```

---

## Filters & Search

### Filter Courses by Difficulty
```bash
GET http://localhost:8000/api/courses/courses/?difficulty=beginner
```

### Filter Courses by Instructor
```bash
GET http://localhost:8000/api/courses/courses/?instructor=1
```

### Filter Lessons by Type
```bash
GET http://localhost:8000/api/courses/lessons/?lesson_type=video
```

---

## Pagination

Most list endpoints support pagination:

```bash
GET http://localhost:8000/api/courses/courses/?page=2
```

Response includes:
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/courses/courses/?page=3",
    "previous": "http://localhost:8000/api/courses/courses/?page=1",
    "results": [...]
}
```

---

## Using with Postman

1. Import the collection
2. Create an environment with:
   - `base_url`: http://localhost:8000
   - `access_token`: (set after login)
3. Use `{{base_url}}` and `{{access_token}}` in requests

## Using with curl

### Set token as variable:
```bash
export TOKEN="your_access_token_here"
```

### Make authenticated request:
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/accounts/users/me/
```

---

## Response Codes

- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Missing/invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource doesn't exist
- `500 Server Error`: Internal error

---

For interactive testing, use Swagger UI at:
http://localhost:8000/swagger/
