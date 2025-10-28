"""
Django management command to seed comprehensive sample data for SmartPath Academy.
Usage: python manage.py seed_sample_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import random

from accounts.models import StudentProfile
from courses.models import (
    Category, Course, Lesson, Quiz, Question, Answer,
    Enrollment, LessonProgress
)
from gamification.models import Badge, UserBadge, Achievement, Leaderboard
from analytics.models import QuizAttempt

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds comprehensive sample data for SmartPath Academy'

    def __init__(self):
        super().__init__()
        self.users = {}
        self.categories = {}
        self.courses = {}
        self.lessons = {}
        self.quizzes = {}
        self.badges = {}

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌱 Starting to seed SmartPath Academy...'))
        
        try:
            with transaction.atomic():
                self.create_users()
                self.create_categories()
                self.create_courses()
                self.create_lessons()
                self.create_quizzes()
                self.create_enrollments()
                self.create_badges()
                self.create_gamification_data()
                
            self.stdout.write(self.style.SUCCESS('\n✅ Sample data seeding completed successfully!'))
            self.print_summary()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error during seeding: {str(e)}'))
            raise

    def create_users(self):
        """Create superuser, instructors, and students"""
        self.stdout.write('\n📝 Creating users...')
        
        # Create superuser
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@smartpath.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'role': 'ADMIN'
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Created superuser: admin'))
        
        # Create instructors
        instructors_data = [
            {
                'username': 'john_doe',
                'email': 'john@smartpath.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'bio': 'Full-stack developer with 10+ years of experience in web development and teaching.',
                'expertise': 'Web Development, JavaScript, Python, Django',
                'rating': 4.8
            },
            {
                'username': 'jane_smith',
                'email': 'jane@smartpath.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'bio': 'Data Science expert and ML engineer passionate about education.',
                'expertise': 'Data Science, Machine Learning, Python, Statistics',
                'rating': 4.9
            }
        ]
        
        for data in instructors_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': 'TEACHER'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created instructor: {data['username']}"))
            
            self.users[data['username']] = user
        
        # Create students
        students_data = [
            {'username': 'alice_wonder', 'first_name': 'Alice', 'last_name': 'Wonder', 'level': 5, 'xp': 1250, 'streak': 7, 'style': 'VISUAL'},
            {'username': 'bob_builder', 'first_name': 'Bob', 'last_name': 'Builder', 'level': 3, 'xp': 650, 'streak': 3, 'style': 'KINESTHETIC'},
            {'username': 'charlie_brown', 'first_name': 'Charlie', 'last_name': 'Brown', 'level': 8, 'xp': 2800, 'streak': 15, 'style': 'AUDITORY'},
            {'username': 'diana_prince', 'first_name': 'Diana', 'last_name': 'Prince', 'level': 6, 'xp': 1850, 'streak': 10, 'style': 'READING_WRITING'},
            {'username': 'evan_peters', 'first_name': 'Evan', 'last_name': 'Peters', 'level': 2, 'xp': 320, 'streak': 1, 'style': 'VISUAL'},
            {'username': 'fiona_apple', 'first_name': 'Fiona', 'last_name': 'Apple', 'level': 4, 'xp': 980, 'streak': 5, 'style': 'AUDITORY'},
            {'username': 'george_lucas', 'first_name': 'George', 'last_name': 'Lucas', 'level': 7, 'xp': 2100, 'streak': 12, 'style': 'VISUAL'},
        ]
        
        for data in students_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': f"{data['username']}@student.com",
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': 'STUDENT'
                }
            )
            if created:
                user.set_password('student123')
                user.save()
                
                StudentProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'current_level': data['level'],
                        'total_xp': data['xp'],
                        'streak_days': data['streak'],
                        'learning_style': data['style']
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created student: {data['username']}"))
            
            self.users[data['username']] = user
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {len(self.users) + 1} users total'))

    def create_categories(self):
        """Create course categories"""
        self.stdout.write('\n📚 Creating categories...')
        
        categories_data = [
            {
                'name': 'Web Development',
                'slug': 'web-development',
                'description': 'Learn to build modern web applications using the latest technologies',
                'icon': 'mdi:web'
            },
            {
                'name': 'Data Science',
                'slug': 'data-science',
                'description': 'Master data analysis, visualization, and machine learning',
                'icon': 'mdi:chart-line'
            },
            {
                'name': 'Mobile Development',
                'slug': 'mobile-development',
                'description': 'Build native and cross-platform mobile applications',
                'icon': 'mdi:cellphone'
            },
            {
                'name': 'Design',
                'slug': 'design',
                'description': 'UI/UX design principles and tools for creating beautiful interfaces',
                'icon': 'mdi:palette'
            },
            {
                'name': 'Business',
                'slug': 'business',
                'description': 'Business skills, entrepreneurship, and management',
                'icon': 'mdi:briefcase'
            }
        ]
        
        for data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                    'icon': data['icon']
                }
            )
            self.categories[data['slug']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created category: {data['name']}"))
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {len(self.categories)} categories'))

    def create_courses(self):
        """Create courses with realistic data"""
        self.stdout.write('\n🎓 Creating courses...')
        
        courses_data = [
            {
                'title': 'Complete Python Web Development with Django',
                'slug': 'python-django-web-development',
                'instructor': 'john_doe',
                'category': 'web-development',
                'description': 'Master Django framework and build full-stack web applications.',
                'learning_objectives': '• Build complete web apps\n• Implement authentication\n• Create REST APIs\n• Deploy to production',
                'difficulty': 'INTERMEDIATE',
                'price': 49.99,
                'duration_hours': 24,
                'is_published': True
            },
            {
                'title': 'JavaScript Mastery: From Basics to Advanced',
                'slug': 'javascript-mastery',
                'instructor': 'john_doe',
                'category': 'web-development',
                'description': 'Comprehensive JavaScript course covering ES6+, async programming, and more.',
                'learning_objectives': '• Master ES6+ features\n• Understand async/await\n• Work with APIs\n• Build interactive UIs',
                'difficulty': 'BEGINNER',
                'price': 0.00,
                'duration_hours': 18,
                'is_published': True
            },
{
                'title': 'React & Redux Complete Guide',
                'slug': 'react-redux-complete',
                'instructor': 'john_doe',
                'category': 'web-development',
                'description': 'Build modern single-page applications with React and Redux.',
                'learning_objectives': '• Build React components\n• Manage state with Redux\n• Use React Hooks\n• Deploy React apps',
                'difficulty': 'INTERMEDIATE',
                'price': 59.99,
                'duration_hours': 20,
                'is_published': True
            },
            {
                'title': 'Data Science with Python: Complete Bootcamp',
                'slug': 'data-science-python-bootcamp',
                'instructor': 'jane_smith',
                'category': 'data-science',
                'description': 'Learn data analysis, visualization, and machine learning.',
                'learning_objectives': '• Analyze data with pandas\n• Create visualizations\n• Build ML models\n• Handle real datasets',
                'difficulty': 'INTERMEDIATE',
                'price': 79.99,
                'duration_hours': 32,
                'is_published': True
            },
            {
                'title': 'Machine Learning A-Z: Hands-On Python',
                'slug': 'machine-learning-python',
                'instructor': 'jane_smith',
                'category': 'data-science',
                'description': 'Complete machine learning course with real projects.',
                'learning_objectives': '• Understand ML algorithms\n• Build predictive models\n• Evaluate performance\n• Deploy ML models',
                'difficulty': 'ADVANCED',
                'price': 89.99,
                'duration_hours': 40,
                'is_published': True
            },
            {
                'title': 'Python for Beginners: Zero to Hero',
                'slug': 'python-beginners',
                'instructor': 'jane_smith',
                'category': 'data-science',
                'description': 'Start your programming journey with Python. No prior experience needed!',
                'learning_objectives': '• Learn Python basics\n• Work with data structures\n• Write functions\n• Build projects',
                'difficulty': 'BEGINNER',
                'price': 0.00,
                'duration_hours': 15,
                'is_published': True
            },
            {
                'title': 'UI/UX Design Fundamentals',
                'slug': 'uiux-design-fundamentals',
                'instructor': 'john_doe',
                'category': 'design',
                'description': 'Learn design principles, user research, and prototyping with Figma.',
                'learning_objectives': '• Master design principles\n• Conduct user research\n• Create wireframes\n• Build prototypes',
                'difficulty': 'BEGINNER',
                'price': 39.99,
                'duration_hours': 16,
                'is_published': True
            },
            {
                'title': 'Business Strategy and Entrepreneurship',
                'slug': 'business-strategy-entrepreneurship',
                'instructor': 'jane_smith',
                'category': 'business',
                'description': 'Learn how to develop business strategies and launch startups.',
                'learning_objectives': '• Develop strategies\n• Create business plans\n• Understand markets\n• Learn startup basics',
                'difficulty': 'INTERMEDIATE',
                'price': 69.99,
                'duration_hours': 20,
                'is_published': True
            }
        ]
        
        for data in courses_data:
            instructor = self.users[data['instructor']]
            category = self.categories[data['category']]
            
            course, created = Course.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'instructor': instructor,
                    'category': category,
                    'description': data['description'],
                    'difficulty_level': data['difficulty'],
                    'estimated_duration': data['duration_hours'],
                    'is_published': data['is_published']
                }
            )
            self.courses[data['slug']] = course
            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created course: {data['title'][:50]}"))
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {len(self.courses)} courses'))

    def create_lessons(self):
        """Create lessons for each course"""
        self.stdout.write('\n📖 Creating lessons...')
        
        lesson_templates = {
            'python-django-web-development': [
                {'title': 'Introduction to Django', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=F5mRW0jo-U4', 'duration': 15, 'order': 1},
                {'title': 'Setting Up Environment', 'type': 'TEXT', 'content': 'Learn how to set up Python and Django...', 'duration': 20, 'order': 2},
                {'title': 'Django Models and ORM', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=rHux0gMZ3Eg', 'duration': 25, 'order': 3},
                {'title': 'Django Knowledge Check', 'type': 'QUIZ', 'duration': 15, 'order': 4},
                {'title': 'Views and Templates', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=F5mRW0jo-U4', 'duration': 35, 'order': 5},
            ],
            'javascript-mastery': [
                {'title': 'JavaScript Basics', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=hdI2bqOjy3c', 'duration': 20, 'order': 1},
                {'title': 'Variables and Data Types', 'type': 'TEXT', 'content': 'Understanding JavaScript data types...', 'duration': 25, 'order': 2},
                {'title': 'Functions and Scope', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=N8ap4k_1QEQ', 'duration': 30, 'order': 3},
                {'title': 'JS Fundamentals Quiz', 'type': 'QUIZ', 'duration': 10, 'order': 4},
            ],
            'react-redux-complete': [
                {'title': 'React Introduction', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=Ke90Tje7VS0', 'duration': 15, 'order': 1},
                {'title': 'Components and Props', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=Ke90Tje7VS0', 'duration': 25, 'order': 2},
                {'title': 'React Hooks', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=O6P86uwfdR0', 'duration': 35, 'order': 3},
                {'title': 'React Basics Quiz', 'type': 'QUIZ', 'duration': 15, 'order': 4},
            ],
            'data-science-python-bootcamp': [
                {'title': 'Introduction to Data Science', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=ua-CiDNNj30', 'duration': 20, 'order': 1},
                {'title': 'Python for Data Analysis', 'type': 'TEXT', 'content': 'Using Python for data manipulation...', 'duration': 30, 'order': 2},
                {'title': 'NumPy and Pandas', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=ZyhVh-qRZPA', 'duration': 40, 'order': 3},
                {'title': 'Data Science Quiz', 'type': 'QUIZ', 'duration': 20, 'order': 4},
            ],
            'machine-learning-python': [
                {'title': 'What is Machine Learning?', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=ukzFI9rgwfU', 'duration': 25, 'order': 1},
                {'title': 'ML Algorithms Overview', 'type': 'TEXT', 'content': 'Understanding different ML algorithms...', 'duration': 30, 'order': 2},
                {'title': 'Linear Regression', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=7ArmBVF2dCs', 'duration': 40, 'order': 3},
                {'title': 'ML Basics Quiz', 'type': 'QUIZ', 'duration': 20, 'order': 4},
            ],
            'python-beginners': [
                {'title': 'Welcome to Python', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=_uQrJ0TkZlc', 'duration': 15, 'order': 1},
                {'title': 'Your First Program', 'type': 'TEXT', 'content': 'Write your first Hello World...', 'duration': 20, 'order': 2},
                {'title': 'Python Basics Quiz', 'type': 'QUIZ', 'duration': 10, 'order': 3},
            ],
            'uiux-design-fundamentals': [
                {'title': 'Introduction to UI/UX', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=c9Wg6Cb_YlU', 'duration': 20, 'order': 1},
                {'title': 'Design Principles', 'type': 'TEXT', 'content': 'Learn fundamental design principles...', 'duration': 25, 'order': 2},
                {'title': 'Design Quiz', 'type': 'QUIZ', 'duration': 15, 'order': 3},
            ],
            'business-strategy-entrepreneurship': [
                {'title': 'Business Strategy Overview', 'type': 'VIDEO', 'video': 'https://www.youtube.com/watch?v=df4J2AQZBLc', 'duration': 25, 'order': 1},
                {'title': 'Market Analysis', 'type': 'TEXT', 'content': 'How to conduct market research...', 'duration': 30, 'order': 2},
                {'title': 'Business Basics Quiz', 'type': 'QUIZ', 'duration': 15, 'order': 3},
            ],
        }
        
        lesson_count = 0
        for course_slug, lessons_data in lesson_templates.items():
            course = self.courses[course_slug]
            for data in lessons_data:
                lesson, created = Lesson.objects.get_or_create(
                    course=course,
                    order=data['order'],
                    defaults={
                        'title': data['title'],
                        'content_type': data['type'],
                        'content': data.get('content', ''),
                        'video_url': data.get('video', ''),
                        'duration': data['duration']
                    }
                )
                if created:
                    lesson_count += 1
                    if data['type'] == 'QUIZ':
                        self.lessons[f"{course_slug}_quiz_{data['order']}"] = lesson
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {lesson_count} lessons'))

    def create_quizzes(self):
        """Create quizzes with questions"""
        self.stdout.write('\n❓ Creating quizzes...')
        
        quiz_count = 0
        question_count = 0
        
        for lesson_key, lesson in self.lessons.items():
            course_slug = lesson_key.split('_quiz_')[0]
            
            quiz, created = Quiz.objects.get_or_create(
                lesson=lesson,
                defaults={
                    'title': f"{lesson.title}",
                    'passing_score': 70,
                    'time_limit': 30
                }
            )
            
            if created:
                quiz_count += 1
                self.quizzes[lesson_key] = quiz
                
                # Add questions
                questions_data = [
                    {
                        'text': f'What is the main concept covered in this course?',
                        'type': 'MULTIPLE_CHOICE',
                        'points': 10,
                        'explanation': 'This tests your understanding of the core concepts.',
                        'answers': [
                            (f'{course_slug.replace("-", " ").title()} fundamentals', True),
                            ('Unrelated topic', False),
                            ('Advanced concepts only', False),
                        ]
                    },
                    {
                        'text': 'True or False: Practice is important for mastering this skill.',
                        'type': 'TRUE_FALSE',
                        'points': 10,
                        'explanation': 'Regular practice is essential for skill development.',
                        'answers': [
                            ('True', True),
                            ('False', False)
                        ]
                    }
                ]
                
                for q_data in questions_data:
                    question = Question.objects.create(
                        quiz=quiz,
                        question_text=q_data['text'],
                        question_type=q_data['type'],
                        points=q_data['points'],
                        explanation=q_data['explanation']
                    )
                    
                    for answer_text, is_correct in q_data['answers']:
                        Answer.objects.create(
                            question=question,
                            answer_text=answer_text,
                            is_correct=is_correct
                        )
                    
                    question_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {quiz_count} quizzes with {question_count} questions'))

    def create_enrollments(self):
        """Create enrollments with progress tracking"""
        self.stdout.write('\n📝 Creating enrollments and progress...')
        
        enrollment_count = 0
        progress_count = 0
        quiz_attempt_count = 0
        
        # Get student users
        students = [u for username, u in self.users.items() if u.role == 'STUDENT']
        courses_list = list(self.courses.values())
        
        for student in students:
            # Enroll each student in 2-3 random courses
            num_enrollments = random.randint(2, 3)
            selected_courses = random.sample(courses_list, num_enrollments)
            
            for idx, course in enumerate(selected_courses):
                # Create enrollment
                is_first_course = (idx == 0)
                progress_pct = random.randint(20, 100) if is_first_course else random.randint(0, 80)
                
                lessons = list(course.lessons.all().order_by('order'))
                completed_lesson_count = int(len(lessons) * progress_pct / 100)
                current_lesson = lessons[min(completed_lesson_count, len(lessons)-1)] if lessons else None
                
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'enrolled_at': timezone.now() - timedelta(days=random.randint(1, 60)),
                        'progress_percentage': progress_pct,
                        'current_lesson': current_lesson,
                        'completed_at': timezone.now() if progress_pct == 100 else None
                    }
                )
                
                if created:
                    enrollment_count += 1
                    
                    # Create lesson progress for completed lessons
                    for lesson in lessons[:completed_lesson_count]:
                        LessonProgress.objects.get_or_create(
                            student=student,
                            lesson=lesson,
                            defaults={
                                'status': 'COMPLETED',
                                'completed_at': timezone.now() - timedelta(days=random.randint(1, 30)),
                                'time_spent': random.randint(10, 60)
                            }
                        )
                        progress_count += 1
                        
                        # If lesson has a quiz, create quiz attempt
                        if lesson.content_type == 'QUIZ' and hasattr(lesson, 'quiz'):
                            score = random.randint(60, 100)
                            QuizAttempt.objects.get_or_create(
                                student=student,
                                quiz=lesson.quiz,
                                defaults={
                                    'score': score,
                                    'percentage': score,
                                    'time_taken': random.randint(600, 1800),
                                    'completed_at': timezone.now() - timedelta(days=random.randint(1, 30)),
                                    'answers': {}
                                }
                            )
                            quiz_attempt_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {enrollment_count} enrollments'))
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {progress_count} lesson progress records'))
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {quiz_attempt_count} quiz attempts'))

    def create_badges(self):
        """Create badge types"""
        self.stdout.write('\n🏆 Creating badges...')
        
        badges_data = [
            {'name': 'First Steps', 'description': 'Complete your first lesson', 'requirement': {'type': 'lesson_count', 'count': 1}, 'points': 10, 'icon': 'mdi:foot-print'},
            {'name': 'Fast Learner', 'description': 'Complete 5 lessons in one day', 'requirement': {'type': 'daily_lessons', 'count': 5}, 'points': 50, 'icon': 'mdi:lightning-bolt'},
            {'name': 'Quiz Master', 'description': 'Score 100% on a quiz', 'requirement': {'type': 'quiz_score', 'score': 100}, 'points': 30, 'icon': 'mdi:trophy'},
            {'name': 'Consistent', 'description': 'Maintain a 7-day streak', 'requirement': {'type': 'streak', 'days': 7}, 'points': 75, 'icon': 'mdi:calendar-check'},
            {'name': 'Dedicated', 'description': 'Maintain a 30-day streak', 'requirement': {'type': 'streak', 'days': 30}, 'points': 200, 'icon': 'mdi:star'},
            {'name': 'Course Completer', 'description': 'Complete your first course', 'requirement': {'type': 'course_count', 'count': 1}, 'points': 100, 'icon': 'mdi:school'},
            {'name': 'Overachiever', 'description': 'Complete 3 courses', 'requirement': {'type': 'course_count', 'count': 3}, 'points': 300, 'icon': 'mdi:medal'},
            {'name': 'Knowledge Seeker', 'description': 'Enroll in 5 courses', 'requirement': {'type': 'enrollment_count', 'count': 5}, 'points': 25, 'icon': 'mdi:book-open'},
            {'name': 'Early Bird', 'description': 'Study before 8 AM', 'requirement': {'type': 'time_of_day', 'before': '08:00'}, 'points': 20, 'icon': 'mdi:weather-sunrise'},
            {'name': 'Night Owl', 'description': 'Study after 10 PM', 'requirement': {'type': 'time_of_day', 'after': '22:00'}, 'points': 20, 'icon': 'mdi:weather-night'},
        ]
        
        badge_count = 0
        for data in badges_data:
            badge, created = Badge.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'requirement': data['requirement'],
                    'points_reward': data['points'],
                    'icon': data.get('icon', 'mdi:star'),
                    'badge_type': 'ACHIEVEMENT'
                }
            )
            self.badges[data['name']] = badge
            if created:
                badge_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {badge_count} badge types'))

    def create_gamification_data(self):
        """Create user badges, achievements, and leaderboard"""
        self.stdout.write('\n🎮 Creating gamification data...')
        
        user_badge_count = 0
        achievement_count = 0
        leaderboard_count = 0
        
        students = [u for username, u in self.users.items() if u.role == 'STUDENT']
        badges_list = list(self.badges.values())
        
        for student in students:
            # Award 2-3 random badges
            num_badges = random.randint(2, 3)
            selected_badges = random.sample(badges_list, num_badges)
            
            for badge in selected_badges:
                UserBadge.objects.get_or_create(
                    user=student,
                    badge=badge,
                    defaults={
                        'earned_at': timezone.now() - timedelta(days=random.randint(1, 30))
                    }
                )
                user_badge_count += 1
            
            # Create 1-2 achievements
            achievement_types = ['COURSE_COMPLETION', 'STREAK', 'QUIZ_MASTER', 'ENGAGEMENT']
            for _ in range(random.randint(1, 2)):
                Achievement.objects.get_or_create(
                    user=student,
                    title=f"{random.choice(achievement_types).replace('_', ' ').title()} Achievement",
                    defaults={
                        'description': f'You have achieved something great!',
                        'achievement_type': random.choice(achievement_types),
                        'points_earned': random.randint(50, 200),
                        'achieved_at': timezone.now() - timedelta(days=random.randint(1, 15))
                    }
                )
                achievement_count += 1
            
            # Create leaderboard entries for different periods
            try:
                profile = student.studentprofile
                for period in ['WEEKLY', 'MONTHLY', 'ALL_TIME']:
                    Leaderboard.objects.get_or_create(
                        user=student,
                        period=period,
                        defaults={
                            'rank': random.randint(1, 100),
                            'total_xp': profile.total_xp if period == 'ALL_TIME' else random.randint(100, profile.total_xp),
                            'courses_completed': Enrollment.objects.filter(student=student, completed_at__isnull=False).count(),
                            'quizzes_passed': QuizAttempt.objects.filter(user=student, passed=True).count()
                        }
                    )
                    leaderboard_count += 1
            except:
                pass
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {user_badge_count} user badges'))
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {achievement_count} achievements'))
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created {leaderboard_count} leaderboard entries'))

    def print_summary(self):
        """Print summary of created data"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('📊 SAMPLE DATA SUMMARY'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        self.stdout.write(f"\n👥 Users:")
        self.stdout.write(f"  • Total users: {User.objects.count()}")
        self.stdout.write(f"  • Students: {User.objects.filter(role='STUDENT').count()}")
        self.stdout.write(f"  • Instructors: {User.objects.filter(role='TEACHER').count()}")
        
        self.stdout.write(f"\n📚 Content:")
        self.stdout.write(f"  • Categories: {Category.objects.count()}")
        self.stdout.write(f"  • Courses: {Course.objects.count()}")
        self.stdout.write(f"  • Lessons: {Lesson.objects.count()}")
        self.stdout.write(f"  • Quizzes: {Quiz.objects.count()}")
        self.stdout.write(f"  • Questions: {Question.objects.count()}")
        
        self.stdout.write(f"\n📈 Engagement:")
        self.stdout.write(f"  • Enrollments: {Enrollment.objects.count()}")
        self.stdout.write(f"  • Lesson Progress: {LessonProgress.objects.count()}")
        self.stdout.write(f"  • Quiz Attempts: {QuizAttempt.objects.count()}")
        
        self.stdout.write(f"\n🏆 Gamification:")
        self.stdout.write(f"  • Badge Types: {Badge.objects.count()}")
        self.stdout.write(f"  • User Badges: {UserBadge.objects.count()}")
        self.stdout.write(f"  • Achievements: {Achievement.objects.count()}")
        self.stdout.write(f"  • Leaderboard Entries: {Leaderboard.objects.count()}")
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('🎉 SmartPath Academy is ready to use!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        self.stdout.write(f"\n🔑 Login Credentials:")
        self.stdout.write(f"  Admin: admin / admin123")
        self.stdout.write(f"  Students: alice_wonder, bob_builder, charlie_brown, etc. / student123")
        self.stdout.write(f"  Instructors: john_doe, jane_smith / password123")
        
        self.stdout.write(f"\n🌐 Access:")
        self.stdout.write(f"  Dashboard: http://localhost:8000/dashboard/")
        self.stdout.write(f"  Courses: http://localhost:8000/courses/")
        self.stdout.write(f"  Admin: http://localhost:8000/admin/\n")
