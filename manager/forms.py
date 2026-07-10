from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Task, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter project title'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your project'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Task details'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }