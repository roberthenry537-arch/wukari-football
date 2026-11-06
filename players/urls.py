from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pitch/<int:pitch_id>/', views.pitch_detail, name='pitch_detail'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
    path('register/', views.register, name='register'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('create-post/', views.create_post, name='create_post'),
]path('logout/', views.logout_view, name='logout'),