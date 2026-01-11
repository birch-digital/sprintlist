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

class UpdateState(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['state']

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

### Board details
@login_required
def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    tasks = Task.objects.filter(board=board).order_by('-timestamp')         # Can remove the order_by for custom ordering if needs be

    return render(request, 'boards/board_detail.html', {'board': board, 'tasks': tasks})

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
            return redirect('boards:board_detail', board_id=board_id)
    else:
        form = TaskForm()

    return render(request, 'boards/add_task.html', {'form': form, 'board': board})

@login_required
def update_task_state(request, board_id, task_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    task = get_object_or_404(Task, id=task_id, board=board)

    if request.method == 'POST':
        form = UpdateState(request.POST, instance=task)

        if form.is_valid():
            form.save()

    return redirect('boards:board_detail', board_id=board_id)


