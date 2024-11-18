from django.shortcuts import render, get_object_or_404, redirect
from .models import BoardGame, Loan
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib import messages  # Check if needed
from django.utils import timezone
from django.http import HttpResponseForbidden


def home(request):
    return render(request, 'board_game_club/home.html')

@login_required
def game_list(request):
    games = BoardGame.objects.all()
    return render(request, 'board_game_club/game_list.html', {'games': games})

@login_required
def game_detail(request, id):
    game = get_object_or_404(BoardGame, id=id)

    # Condition of if the book is loneaed
    active_loan = game.loans.filter(returned_at__isnull=True).first()

    return render(request, 'board_game_club/game_detail.html', {
        'game': game,
        'borrower': active_loan.borrower if active_loan else None,  # get who borrows it
    })







@login_required
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



@login_required
def edit_game(request, id):
    game = get_object_or_404(BoardGame, id=id)

    # Only the person who made the game can edit the board game
    if game.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit this game. Use back page to go back.")

    if request.method == 'POST':
        # Get the data
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Update the edited aspects
        game.title = title
        game.description = description
        game.save()

        # Go back to the games details
        return redirect('game_detail', id=game.id)
    return render(request, 'board_game_club/edit_game.html', {'game': game})


@login_required
def borrow_game(request, id):
    game = get_object_or_404(BoardGame, id=id)

    # Logic to check if board game is borrowed
    if not game.is_available:
        messages.error(request, "This board game is already borrowed.")
        return redirect('game_list')

    # Limit to 3 books
    active_loans = Loan.objects.filter(borrower=request.user, returned_at__isnull=True).count()
    if active_loans >= 3: #limit 3
        messages.error(request, "You can only borrow up to 3 games at a time, delete or return a book")
        return redirect('game_list')

    # Loan it
    Loan.objects.create(borrower=request.user, game=game)
    game.is_available = False
    game.save()

    messages.success(request, f"You have successfully borrowed '{game.title}'.")
    return redirect('game_list')

@login_required
def return_game(request, id):
    game = get_object_or_404(BoardGame, id=id)

    # Check if the user has borrowed this game
    loan = Loan.objects.filter(game=game, borrower=request.user, returned_at__isnull=True).first()
    if not loan:
        messages.error(request, "You cannot return a game you haven't borrowed.")
        return redirect('game_list')

    # Mark the game as returned and update its availability
    loan.returned_at = timezone.now()
    loan.save()
    game.is_available = True
    game.save()

    messages.success(request, f"You have successfully returned '{game.title}'.")
    return redirect('game_list')



@login_required
def delete_game(request, id):
    game = get_object_or_404(BoardGame, id=id)

    # Ensure only the owner can delete the game
    if game.owner != request.user:
        messages.error(request, "You are not allowed to delete this game.")
        return redirect('game_list')

    if request.method == 'POST':
        game.delete()
        messages.success(request, "Game deleted successfully!")
        return redirect('game_list')

    return render(request, 'board_game_club/delete_game.html', {'game': game})




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