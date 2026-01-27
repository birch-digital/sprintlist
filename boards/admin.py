from django.contrib import admin
from .models import Board, Sprint, Task

# AI
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'description')
    list_filter = ('owner',)


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'start_date', 'due_date', 'get_owner')
    list_filter = ('board', 'start_date')
    
    def get_owner(self, obj):
        return obj.board.owner
    get_owner.short_description = 'Owner'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_title', 'sprint', 'get_board', 'state', 'timestamp')
    list_filter = ('sprint__board', 'state')
    
    def get_board(self, obj):
        return obj.sprint.board
    get_board.short_description = 'Board'