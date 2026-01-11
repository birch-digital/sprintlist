# IMPORTS
## Django
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

## App
from .models import Board, Task

########

# VIEWS
## Forms
### Adding Boards
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description']

### Adding Tasks
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'task_details', 'state']

## Functions
### Dashboard display
@login_required
def dashboard(request):
    boards = Board.objects.filter(owner=request.user).order_by('title')
    form = BoardForm()

    return render(request, 'boards/dashboard.html', {'boards': boards, 'form': form})

### Board creation
@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)

        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()

    return redirect('boards:dashboard')

### Task creation
@login_required
def add_task(request, board_id):
    board = Board.objects.get(id=board_id, owner=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.board = board
            task.save()
            return redirect('boards:dashboard')
    else:
        form = TaskForm()

    return render(request, 'boards/add_task.html', {'form': form, 'board': board})


