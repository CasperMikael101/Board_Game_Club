from django.shortcuts import render, get_object_or_404, redirect
from .models import BoardGame
from django.contrib.auth import login
from .forms import RegisterForm



def home(request):
    return render(request, 'board_game_club/home.html')


def game_list(request):
    games = BoardGame.objects.all()
    return render(request, 'board_game_club/game_list.html', {'games': games})

def game_detail(request, id):
    game = get_object_or_404(BoardGame, id=id)
    return render(request, 'board_game_club/game_detail.html', {'game': game})

def add_game(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Create and save a new BoardGame instance
        game = BoardGame.objects.create(title=title, description=description, owner=request.user)
        game.save()
        
        # Redirect to the game list page after saving
        return redirect('game_list')
    
    return render(request, 'board_game_club/add_game.html')

def edit_game(request, id):
    # Logic to edit a game
    return render(request, 'board_game_club/edit_game.html')

def borrow_game(request, id):
    # Logic to borrow a game
    return redirect('game_list')

def return_game(request, id):
    # Logic to return a game
    return redirect('game_list')





def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user to the database
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to homepage after registration
    else:
        form = RegisterForm()
    return render(request, 'board_game_club/register.html', {'form': form})