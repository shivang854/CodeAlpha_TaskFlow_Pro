from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Project, Task
from .forms import RegisterForm, ProjectForm, TaskForm, CommentForm


def home(request):
    if request.user.is_authenticated:
        recent_projects = Project.objects.filter(owner=request.user).order_by('-created_at')[:3]
    else:
        recent_projects = []
    return render(request, 'manager/home.html', {'recent_projects': recent_projects})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'manager/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'manager/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')


@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'manager/project_list.html', {'projects': projects})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, "Project created successfully.")
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()

    return render(request, 'manager/create_project.html', {'form': form})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    tasks = project.tasks.all().order_by('-created_at')

    todo_count = tasks.filter(status='todo').count()
    progress_count = tasks.filter(status='in_progress').count()
    done_count = tasks.filter(status='done').count()

    context = {
        'project': project,
        'tasks': tasks,
        'todo_count': todo_count,
        'progress_count': progress_count,
        'done_count': done_count,
    }
    return render(request, 'manager/project_detail.html', context)


@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, "Task created successfully.")
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()

    return render(request, 'manager/create_task.html', {
        'form': form,
        'project': project
    })


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)
    comments = task.comments.all().order_by('-created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added.")
            return redirect('task_detail', task_id=task.id)
    else:
        comment_form = CommentForm()

    return render(request, 'manager/task_detail.html', {
        'task': task,
        'comments': comments,
        'comment_form': comment_form
    })


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__owner=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'manager/edit_task.html', {
        'form': form,
        'task': task
    })
