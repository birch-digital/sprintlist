# IMPORTS
from django.urls import path

from . import views

# GLOBAL
app_name = 'boards'

# URLS
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_board, name='create_board'),
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    path('board/<int:board_id>/tasks/add/', views.add_task, name='add_task'),
    path('board/<int:board_id>/tasks/<int:task_id>/state/', views.update_task_state, name='update_task_state'),
]