"""
Course views for frontend templates
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Course, Lesson, Quiz, Question, Enrollment, LessonProgress
from analytics.models import QuizAttempt


def course_detail(request, slug):
    """Course detail page"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    
    is_enrolled = False
    enrollment = None
    completed_lessons = []
    current_lesson = None
    
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course)
            is_enrolled = True
            completed_lessons = list(LessonProgress.objects.filter(
                user=request.user,
                lesson__course=course,
                status='COMPLETED'
            ).values_list('lesson_id', flat=True))
            current_lesson = enrollment.current_lesson
        except Enrollment.DoesNotExist:
            pass
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'completed_lessons': completed_lessons,
        'current_lesson': current_lesson,
        'title': course.title,
        'subTitle': 'Course Details',
    }
    
    return render(request, 'courses/course_detail.html', context)


@login_required
def course_enroll(request, slug):
    """Enroll in a course"""
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=slug, is_published=True)
        
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={
                'current_lesson': course.lessons.first()
            }
        )
        
        if created:
            messages.success(request, f'Successfully enrolled in {course.title}!')
        else:
            messages.info(request, f'You are already enrolled in {course.title}')
        
        return redirect('course-detail', slug=slug)
    
    return redirect('course-list')


@login_required
def lesson_view(request, lesson_id):
    """View a lesson"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    
    # Check enrollment
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'Please enroll in the course first')
        return redirect('course-detail', slug=course.slug)
    
    # Get completed lessons
    completed_lessons = list(LessonProgress.objects.filter(
        user=request.user,
        lesson__course=course,
        status='COMPLETED'
    ).values_list('lesson_id', flat=True))
    
    # Get accessible lessons (completed + current)
    accessible_lessons = completed_lessons + [enrollment.current_lesson.id]
    
    # Check if this lesson is accessible
    if lesson.id not in accessible_lessons:
        messages.warning(request, 'Please complete previous lessons first')
        return redirect('lesson-view', lesson_id=enrollment.current_lesson.id)
    
    # Check if completed
    is_completed = lesson.id in completed_lessons
    
    # Get previous and next lessons
    all_lessons = list(course.lessons.all().order_by('order'))
    current_index = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), None)
    
    previous_lesson = all_lessons[current_index - 1] if current_index and current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index is not None and current_index < len(all_lessons) - 1 else None
    
    context = {
        'lesson': lesson,
        'course': course,
        'enrollment': enrollment,
        'completed_lessons': completed_lessons,
        'accessible_lessons': accessible_lessons,
        'is_completed': is_completed,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'current_lesson': enrollment.current_lesson,
        'title': lesson.title,
        'breadcrumbs': [
            {'name': course.title, 'url': f'/courses/{course.slug}/'},
            {'name': lesson.title, 'url': None},
        ]
    }
    
    return render(request, 'courses/lesson_view.html', context)


@login_required
def lesson_complete(request, lesson_id):
    """Mark lesson as complete"""
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)
        course = lesson.course
        
        # Check enrollment
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course)
        except Enrollment.DoesNotExist:
            messages.error(request, 'You must be enrolled in this course')
            return redirect('course-detail', slug=course.slug)
        
        # Mark as complete
        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'status': 'COMPLETED'}
        )
        
        if not created and progress.status != 'COMPLETED':
            progress.status = 'COMPLETED'
            progress.save()
        
        # Update enrollment current lesson
        all_lessons = list(course.lessons.all().order_by('order'))
        current_index = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), None)
        
        if current_index is not None and current_index < len(all_lessons) - 1:
            enrollment.current_lesson = all_lessons[current_index + 1]
            enrollment.save()
        
        messages.success(request, f'Lesson "{lesson.title}" marked as complete! 🎉')
        
        # Redirect to next lesson or course detail
        if current_index is not None and current_index < len(all_lessons) - 1:
            return redirect('lesson-view', lesson_id=all_lessons[current_index + 1].id)
        else:
            return redirect('course-detail', slug=course.slug)
    
    return redirect('course-list')


@login_required
def quiz_take(request, quiz_id):
    """Take a quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all().prefetch_related('answers')
    
    submitted = False
    results = None
    
    if request.method == 'POST':
        # Process quiz submission
        submitted = True
        correct_count = 0
        total_questions = questions.count()
        question_results = []
        
        for question in questions:
            user_answer_id = request.POST.get(f'question_{question.id}')
            user_answer = None
            correct_answer = None
            is_correct = False
            
            if question.question_type == 'MULTIPLE_CHOICE':
                try:
                    user_answer_obj = question.answers.get(id=user_answer_id)
                    user_answer = user_answer_obj.answer_text
                    correct_answer_obj = question.answers.filter(is_correct=True).first()
                    correct_answer = correct_answer_obj.answer_text if correct_answer_obj else None
                    is_correct = user_answer_obj.is_correct
                except:
                    pass
            
            if is_correct:
                correct_count += 1
            
            question_results.append({
                'text': question.question_text,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.explanation,
            })
        
        score = correct_count
        percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        passed = percentage >= (quiz.passing_score or 70)
        xp_earned = int(percentage * 2) if passed else int(percentage)
        
        # Save quiz attempt
        QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_count,
            percentage=percentage,
            passed=passed,
            time_taken=0,  # TODO: Track actual time
            answers_given={}
        )
        
        results = {
            'score': score,
            'percentage': round(percentage, 1),
            'correct_count': correct_count,
            'total': total_questions,
            'passed': passed,
            'xp_earned': xp_earned,
            'questions': question_results,
        }
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'submitted': submitted,
        'results': results,
        'title': quiz.title,
        'subTitle': 'Quiz',
    }
    
    return render(request, 'courses/quiz_take.html', context)
