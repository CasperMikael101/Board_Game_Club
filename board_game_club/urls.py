from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),                    # Homepage
    path('login/', LoginView.as_view(template_name='board_game_club/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('games/', views.game_list, name='game_list'),    # List of games
    path('games/<int:id>/', views.game_detail, name='game_detail'),  # Game details
    path('games/add/', views.add_game, name='add_game'),  # Add a new game
    path('games/<int:id>/edit/', views.edit_game, name='edit_game'), # Edit a game
    path('games/<int:id>/borrow/', views.borrow_game, name='borrow_game'), # Borrow a game
    path('games/<int:id>/return/', views.return_game, name='return_game'), # Return a game
    path('games/<int:id>/delete/', views.delete_game, name='delete_game'), # To delete a game

]
