# IMPORTS
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms

from .models import Board

# VIEWS
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description']

@login_required
def dashboard(request):
    boards = Board.objects.filter(owner=request.user).order_by('title')
    form = BoardForm()

    return render(request, 'boards/dashboard.html', {'boards': boards, 'form': form})

@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)

        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()

    return redirect('boards:dashboard')

