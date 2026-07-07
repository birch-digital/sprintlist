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
    
# Services a user offers (e.g. "Blog", "Booking System"); chosen per-project
## to auto-generate that project's sprints
class Service(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=40)
    estimated_days = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

## Predefined checklist of task titles attached to a service; copied into
## real Tasks whenever a sprint is generated from this service
class ServiceTask(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='template_tasks'
    )
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# Specific chunks of a project, broken down into tasks
class Sprint(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='sprints'
    )
    ## Service this sprint was generated from, if any; kept on delete so
    ## historical sprints aren't lost if the service is later removed
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sprints'
    )
    title = models.CharField(max_length=40)
    start_date = models.DateField(db_default=Now())
    ## No default/required constraint: real scheduling comes from calendar
    ## integration, which doesn't exist yet
    due_date = models.DateField(null=True, blank=True)
    ## Snapshot of service.estimated_days at creation time, so later edits
    ## to the service don't retroactively change past sprints
    planned_days = models.PositiveIntegerField(null=True, blank=True)

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
    task_details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    state = models.IntegerField(choices=State.choices, default=State.TODO)

    def __str__(self):
        return self.task_title

