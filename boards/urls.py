# IMPORTS
from django.urls import path

from . import views

# GLOBAL
app_name = 'boards'

# URLS
urlpatterns = [
    path(
        '', 
        views.dashboard, 
        name='dashboard',
    ),
    path(
        'create/', 
        views.create_board, 
        name='create_board',
    ),
    # Boards
    path(
        'board/<int:board_id>/', 
        views.board_detail, 
        name='board_detail',
    ),
    # Sprints
    path(
        'board/<int:board_id>/sprints/create/', 
        views.create_sprint, 
        name='create_sprint',
    ),
    path(
        'board/<int:board_id>/sprint/<int:sprint_id>/', 
        views.sprint_detail, 
        name='sprint_detail',
    ),
    path(
        'board/<int:board_id>/sprints/<int:sprint_id>/delete/',
        views.delete_sprint,
        name='delete_sprint'
    ),
    # Tasks
    path(
        'board/<int:board_id>/sprint/<int:sprint_id>/tasks/add/', 
        views.add_task, 
        name='add_task',
    ),
    path(
        'board/<int:board_id>/sprint/<int:sprint_id>/tasks/<int:task_id>/state/', 
        views.update_task_state, 
        name='update_task_state',
    ),
]