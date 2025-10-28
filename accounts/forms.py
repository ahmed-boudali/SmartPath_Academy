"""
Forms for user authentication and profile management
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()


class CustomLoginForm(AuthenticationForm):
    """Custom login form with WowDash styling"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email or username',
            'id': 'username'
        }),
        label='Email or Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'password'
        }),
        label='Password'
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'rememberMe'
        }),
        label='Remember me'
    )


class UserRegistrationForm(UserCreationForm):
    """Student registration form with learning style assessment"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'id': 'email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username',
            'id': 'username'
        })
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
            'id': 'firstName'
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
            'id': 'lastName'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password',
            'id': 'password1'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'password2'
        })
    )
    
    # Learning style assessment
    learning_question_1 = forms.ChoiceField(
        choices=[
            ('VISUAL', 'Watch video demonstrations'),
            ('AUDITORY', 'Listen to explanations'),
            ('KINESTHETIC', 'Try it hands-on'),
            ('READING_WRITING', 'Read detailed instructions'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='When learning something new, I prefer to:'
    )
    
    learning_question_2 = forms.ChoiceField(
        choices=[
            ('VISUAL', 'See diagrams or charts'),
            ('AUDITORY', 'Hear them explained'),
            ('KINESTHETIC', 'Do practical exercises'),
            ('READING_WRITING', 'Write notes'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='I remember things best when I:'
    )
    
    learning_question_3 = forms.ChoiceField(
        choices=[
            ('VISUAL', 'I like colorful presentations and visual aids'),
            ('AUDITORY', 'I enjoy discussions and verbal explanations'),
            ('KINESTHETIC', 'I learn by doing and experimenting'),
            ('READING_WRITING', 'I prefer reading books and taking notes'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Which statement describes you best?'
    )
    
    learning_question_4 = forms.ChoiceField(
        choices=[
            ('VISUAL', 'Watching tutorial videos'),
            ('AUDITORY', 'Listening to podcasts or lectures'),
            ('KINESTHETIC', 'Building projects and coding along'),
            ('READING_WRITING', 'Reading documentation and articles'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='I learn programming best through:'
    )
    
    preferred_pace = forms.ChoiceField(
        choices=[
            ('SLOW', 'Slow - I like to take my time'),
            ('MEDIUM', 'Medium - Balanced pace'),
            ('FAST', 'Fast - I want to learn quickly'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='What is your preferred learning pace?'
    )
    
    skill_level = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-range',
            'type': 'range',
            'id': 'skillLevel'
        }),
        label='Rate your current programming skill level (1-10)'
    )
    
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'termsAccepted'
        }),
        label='I agree to the Terms of Service and Privacy Policy'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def determine_learning_style(self):
        """Determine learning style based on quiz answers"""
        answers = [
            self.cleaned_data.get('learning_question_1'),
            self.cleaned_data.get('learning_question_2'),
            self.cleaned_data.get('learning_question_3'),
            self.cleaned_data.get('learning_question_4'),
        ]
        
        # Count occurrences of each style
        style_counts = {}
        for answer in answers:
            style_counts[answer] = style_counts.get(answer, 0) + 1
        
        # Return the most common style
        return max(style_counts, key=style_counts.get)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = 'STUDENT'
        
        if commit:
            user.save()
            
            # Create student profile with assessment results
            StudentProfile.objects.create(
                user=user,
                learning_style=self.determine_learning_style(),
                preferred_pace=self.cleaned_data['preferred_pace'],
                current_level=min(self.cleaned_data['skill_level'], 10)
            )
        
        return user


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class StudentProfileForm(forms.ModelForm):
    """Form for editing student profile settings"""
    
    class Meta:
        model = StudentProfile
        fields = ['learning_style', 'preferred_pace']
        widgets = {
            'learning_style': forms.Select(attrs={'class': 'form-select'}),
            'preferred_pace': forms.Select(attrs={'class': 'form-select'}),
        }
