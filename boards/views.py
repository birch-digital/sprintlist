###############################################################################
# ------
# IMPORTS
# ------

## ---
## Django
## ---
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

## ---
## App
## ---
from .models import *


###############################################################################
# ------
# FORMS
# ------

## ---
## Adding Boards
## ---
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description']

## ---
## Adding Sprints
## ---
class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['title', 'start_date', 'due_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

## ---
## Adding Tasks
## ---
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'task_details', 'state']

class UpdateState(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['state']


###############################################################################
# ------
# FUNCTIONS
# ------

## ---
## Dashboard display
## ---
@login_required
def dashboard(request):
    boards = Board.objects.filter(owner=request.user).order_by('title')

    for board in boards:
        tasks = Task.objects.filter(sprint__board=board)
        todo_task_count = 0
        wip_task_count = 0
        done_task_count = 0

        for task in tasks:
            if (task.state == 0):
                todo_task_count += 1
            elif (task.state == 1):
                wip_task_count += 1
            else:
                done_task_count += 1

        board.todo = todo_task_count
        board.wip = wip_task_count
        board.done = done_task_count
        board.total = tasks.count()

        def create_bar(status, percent):
            return f'<div class="bar {status}" style="width:{percent}%"></div>'

        if board.total > 0:
            todo_percent = (todo_task_count / board.total) * 100
            wip_percent = (wip_task_count / board.total) * 100
            done_percent = (done_task_count / board.total) * 100

            board.todostyle = create_bar('todo', todo_percent)
            board.wipstyle = create_bar('wip', wip_percent)
            board.donestyle = create_bar('done', done_percent)

    form = BoardForm()

    return render(
        request, 
        'boards/dashboard.html', 
        {'boards': boards, 'form': form}
    )

## ---
## Board creation
## ---
@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()

    return redirect('boards:dashboard')

## ---
## Board details
## ---
@login_required
def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    sprints = Sprint.objects.filter(board=board).order_by('id')
    tasks = Task.objects.filter(sprint__board=board).order_by('-timestamp')

    class TaskCounts:
        pass

    counts = TaskCounts()
    counts.todo = tasks.filter(state=0).count()
    counts.wip = tasks.filter(state=1).count()
    counts.done = tasks.filter(state=2).count()

    return render(
        request, 
        'boards/board_detail.html', 
        {'board': board, 'sprints': sprints, 'tasks': tasks, 'counts': counts}
    )

## ---
## Sprint Creation
## ---
@login_required
def create_sprint(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)

    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.board = board
            sprint.save()
    
    return redirect('boards:board_detail', board_id=board_id)

@login_required
def sprint_detail(request, board_id, sprint_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    sprint = get_object_or_404(Sprint, id=sprint_id, board=board)
    tasks = Task.objects.filter(sprint=sprint)

    class TaskCounts:
        pass

    counts = TaskCounts()
    counts.todo = tasks.filter(state=0).count()
    counts.wip = tasks.filter(state=1).count()
    counts.done = tasks.filter(state=2).count()

    return render(
        request,
        'boards/sprint_detail.html',
        {'board': board, 'sprint': sprint, 'tasks': tasks, 'counts': counts}
    )

## ---
## Task creation and updating
## ---
@login_required
def add_task(request, board_id, sprint_id):
    board = Board.objects.get(id=board_id, owner=request.user)
    sprint = get_object_or_404(Sprint, id=sprint_id, board=board)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.sprint = sprint
            task.save()
            
            return redirect(
                'boards:sprint_detail', 
                board_id=board_id,
                sprint_id=sprint_id
            )
    else:
        form = TaskForm()

    return render(
        request, 
        'boards/add_task.html', 
        {'form': form, 'board': board, 'sprint': sprint}
    )

@login_required
def update_task_state(request, board_id, sprint_id, task_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    sprint = get_object_or_404(Sprint, id=sprint_id, board=board)
    task = get_object_or_404(Task, id=task_id, sprint=sprint)

    if request.method == 'POST':
        form = UpdateState(request.POST, instance=task)

        if form.is_valid():
            form.save()
        return redirect(
            'boards:sprint_detail', 
            board_id=board_id, 
            sprint_id=sprint_id
        )


