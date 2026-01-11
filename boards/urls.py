# IMPORTS
from django.urls import path

from . import views

#
app_name = 'boards'

# URLS
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_board, name='create_board'),
    path('<int:board_id>/tasks/add/', views.add_task, name='add_task')
]