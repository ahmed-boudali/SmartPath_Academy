"""
Custom authentication views for SmartPath Academy
"""

from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import CustomLoginForm, UserRegistrationForm, UserProfileForm, StudentProfileForm
from .models import StudentProfile
from courses.models import Course


class CustomLoginView(LoginView):
    """Custom login view with WowDash styling"""
    form_class = CustomLoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('student-dashboard')
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        
        messages.success(self.request, f'Welcome back, {form.get_user().first_name}!')
        return super().form_valid(form)


class RegisterView(CreateView):
    """Student registration view with learning style assessment"""
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('onboarding')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Auto-login after registration
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(
                self.request,
                f'Welcome to SmartPath Academy, {user.first_name}! Let\'s get you started.'
            )
        
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    """Student profile management view"""
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')
    form_class = UserProfileForm
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user statistics
        from courses.models import Enrollment, LessonProgress
        from gamification.models import UserBadge, Achievement
        
        user = self.request.user
        
        context['profile_form'] = UserProfileForm(instance=user)
        
        try:
            student_profile = user.studentprofile
            context['student_profile_form'] = StudentProfileForm(instance=student_profile)
            context['student_profile'] = student_profile
        except:
            context['student_profile_form'] = None
            context['student_profile'] = None
        
        # User statistics
        context['stats'] = {
            'courses_enrolled': Enrollment.objects.filter(student=user).count(),
            'courses_completed': Enrollment.objects.filter(
                student=user,
                completed_at__isnull=False
            ).count(),
            'lessons_completed': LessonProgress.objects.filter(
                student=user,
                status='COMPLETED'
            ).count(),
            'badges_earned': UserBadge.objects.filter(user=user).count(),
            'achievements': Achievement.objects.filter(user=user).order_by('-achieved_at')[:5],
        }
        
        # Recent badges
        context['recent_badges'] = UserBadge.objects.filter(user=user).select_related('badge').order_by('-earned_at')[:6]
        
        context['title'] = 'My Profile'
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        profile_form = UserProfileForm(request.POST, instance=request.user)
        
        student_profile_form = None
        try:
            student_profile = request.user.studentprofile
            student_profile_form = StudentProfileForm(request.POST, instance=student_profile)
        except:
            pass
        
        if profile_form.is_valid() and (student_profile_form is None or student_profile_form.is_valid()):
            profile_form.save()
            if student_profile_form:
                student_profile_form.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            return self.render_to_response(
                self.get_context_data(
                    profile_form=profile_form,
                    student_profile_form=student_profile_form
                )
            )


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view with WowDash styling"""
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Password reset instructions have been sent to your email.'
        )
        return super().form_valid(form)


@login_required
def onboarding_view(request):
    """Onboarding flow for new students"""
    try:
        student_profile = request.user.studentprofile
        
        # Get course recommendations based on learning style and level
        recommended_courses = Course.objects.filter(
            is_published=True,
            difficulty_level='BEGINNER' if student_profile.current_level <= 3 else 'INTERMEDIATE'
        ).select_related('category', 'instructor')[:6]
        
        context = {
            'student_profile': student_profile,
            'recommended_courses': recommended_courses,
            'title': 'Welcome to SmartPath Academy',
        }
        
        return render(request, 'accounts/onboarding.html', context)
        
    except:
        # If no profile exists, redirect to dashboard
        return redirect('student-dashboard')
