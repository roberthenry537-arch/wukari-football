from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Player Search and Discovery
    path('players/search/', views.player_search, name='player_search'),

    # Clubs
    path('clubs/', views.club_list, name='club_list'),
    path('club/<int:club_id>/', views.club_detail, name='club_detail'),

    # Football Fixtures and Results
    path('fixtures/', views.fixture_list, name='fixture_list'),

    # Pitches
    path('pitch/<int:pitch_id>/', views.pitch_detail, name='pitch_detail'),

    # Player Profiles
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),

    # Registration and Profiles
    path('register/', views.register, name='register'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # Posts
    path('create-post/', views.create_post, name='create_post'),

    # Post Likes and Comments
    path('post/<int:post_id>/like/', views.post_like, name='post_like'),
    path('post/<int:post_id>/comment/', views.post_comment, name='post_comment'),

    # Logout
    path('logout/', views.logout_view, name='player_logout'),

    # Become a Referee
    path('become-referee/', views.become_referee, name='become_referee'),
    path('referees/', views.referee_list, name='referee_list'),
    path('club/<int:club_id>/download/', views.download_club_players, name='download_club_players'),
    path('tournament/<int:tournament_id>/submit-squad/', views.submit_squad, name='submit_squad'),
    path('tournaments/', views.tournament_list, name='tournament_list'),
    path('tournament/<int:tournament_id>/squads/', views.tournament_squads, name='tournament_squads'),
    path('squad/<int:squad_id>/download/', views.download_squad, name='download_squad'),
]