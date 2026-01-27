# Imports
## Django imports
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.functions import Now

# Auth user setup
User = get_user_model()

# Models
## Board = project: Projects can contain many sprints, sprints contain tasks; 
## users can have multiple projects
class Board(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
# Specific chunks of a project, broken down into tasks
## TODO: Add timeframes
class Sprint(models.Model):
    board = models.ForeignKey(
        Board, 
        on_delete=models.CASCADE, 
        related_name='sprints'
    )
    title = models.CharField(max_length=40)
    start_date = models.DateField(db_default=Now())
    due_date = models.DateField()

    def __str__(self):
        return self.title

## Tasks: Have state and belong to only one project
class Task(models.Model):
    class State(models.IntegerChoices):
        TODO = 0
        WIP = 1
        DONE = 2

    sprint = models.ForeignKey(
        Sprint, 
        on_delete=models.CASCADE, 
        related_name='tasks'
    )
    task_title = models.CharField(max_length=100)
    task_details = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    state = models.IntegerField(choices=State.choices, default=State.TODO)

    def __str__(self):
        return self.task_title

