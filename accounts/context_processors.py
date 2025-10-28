"""
Context processors to add data to all templates
"""
from accounts.models import StudentProfile


def navigation_context(request):
    """Add navigation-related context to all templates"""
    context = {}
    
    if request.user.is_authenticated:
        try:
            profile = request.user.studentprofile
            context['student_profile'] = profile
            context['user_level'] = profile.current_level or 1
            context['user_xp'] = profile.total_xp or 0
            context['user_streak'] = profile.current_streak or 0
        except:
            context['student_profile'] = None
            context['user_level'] = 1
            context['user_xp'] = 0
            context['user_streak'] = 0
        
        # Add notifications count
        context['notifications_count'] = 0  # TODO: Implement notifications
        context['notifications'] = []
    
    return context
