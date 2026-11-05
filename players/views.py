from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Pitch, PlayerProfile, Post
from django import forms


class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = [
            'full_name', 'role', 'age', 'position', 'preferred_foot',
            'height', 'phone_number', 'religion', 'state_of_origin',
            'bio', 'current_pitch', 'goals_scored', 'appearances', 'profile_photo'
        ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'caption', 'image', 'video']


def home(request):
    pitches = Pitch.objects.all()
    return render(request, 'players/home.html', {'pitches': pitches})


def pitch_detail(request, pitch_id):
    pitch = get_object_or_404(Pitch, id=pitch_id)
    players = pitch.players.all()
    return render(request, 'players/pitch_detail.html', {
        'pitch': pitch,
        'players': players
    })


def player_detail(request, player_id):
    player = get_object_or_404(PlayerProfile, id=player_id)
    return render(request, 'players/player_detail.html', {'player': player})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_profile')
        else:
            # Form has errors
            return render(request, 'players/register.html', {'form': form})
    else:
        form = UserCreationForm()

    return render(request, 'players/register.html', {'form': form})

@login_required
def create_profile(request):
    if hasattr(request.user, 'playerprofile'):
        return redirect('edit_profile')

    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
    else:
        form = PlayerProfileForm()

    return render(request, 'players/create_profile.html', {'form': form})


@login_required
def edit_profile(request):
    profile = get_object_or_404(PlayerProfile, user=request.user)

    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('player_detail', player_id=profile.id)
    else:
        form = PlayerProfileForm(instance=profile)

    return render(request, 'players/create_profile.html', {'form': form, 'editing': True})


@login_required
def create_post(request):
    if not hasattr(request.user, 'playerprofile'):
        return redirect('create_profile')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.playerprofile
            post.save()
            return redirect('player_detail', player_id=request.user.playerprofile.id)
    else:
        form = PostForm()

    return render(request, 'players/create_post.html', {'form': form})