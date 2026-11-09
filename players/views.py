from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django import forms
from django.utils import timezone

from .models import (
    Pitch,
    PlayerProfile,
    Post,
    PostLike,
    PostComment,
    Club,
    Fixture,
)


# PLAYER PROFILE FORM
class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = [
    'full_name', 'role', 'age', 'position', 'preferred_foot',
    'height', 'phone_number', 'religion', 'state_of_origin',
    'bio', 'current_pitch', 'club', 'goals_scored', 'appearances', 'profile_photo'
]


# SECURE POST FORM
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'caption', 'image', 'video']

    def clean(self):
        cleaned_data = super().clean()

        post_type = cleaned_data.get('post_type')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        if post_type == 'PHOTO':
            if not image:
                self.add_error('image', 'Please upload a photo.')
            if video:
                self.add_error(
                    'video',
                    'Remove the video from this photo post.'
                )

        elif post_type == 'VIDEO':
            if not video:
                self.add_error('video', 'Please upload a video.')
            if image:
                self.add_error(
                    'image',
                    'Remove the photo from this video post.'
                )

        return cleaned_data


# HOME PAGE AND DASHBOARD STATISTICS
def home(request):
    pitches = Pitch.objects.all()

    home_posts = Post.objects.select_related(
        'author', 'author__user'
    ).prefetch_related(
        'likes', 'comments__user'
    ).order_by('-created_at')[:6]

    liked_post_ids = set()

    if request.user.is_authenticated:
        liked_post_ids = set(
            PostLike.objects.filter(
                user=request.user,
                post__in=home_posts
            ).values_list('post_id', flat=True)
        )

    total_players = PlayerProfile.objects.filter(
        role='PLAYER'
    ).count()

    total_coaches = PlayerProfile.objects.exclude(
        role='PLAYER'
    ).count()

    total_clubs = Club.objects.count()
    total_pitches = Pitch.objects.count()

    featured_players = PlayerProfile.objects.filter(
        role='PLAYER'
    ).order_by('-id')[:4]

    upcoming_home_fixtures = Fixture.objects.filter(
        status='UPCOMING',
        match_date__gte=timezone.localdate()
    ).select_related(
        'home_club', 'away_club'
    ).order_by(
        'match_date', 'match_time'
    )[:4]

    recent_home_results = Fixture.objects.filter(
        status='COMPLETED'
    ).select_related(
        'home_club', 'away_club'
    ).order_by(
        '-match_date', '-match_time'
    )[:4]

    return render(request, 'players/home.html', {
        'pitches': pitches,
        'home_posts': home_posts,
        'liked_post_ids': liked_post_ids,
        'total_players': total_players,
        'total_coaches': total_coaches,
        'total_clubs': total_clubs,
        'total_pitches': total_pitches,
        'featured_players': featured_players,
        'upcoming_home_fixtures': upcoming_home_fixtures,
        'recent_home_results': recent_home_results,
    })


# LIKE OR UNLIKE A FOOTBALL POST
@login_required
@require_POST
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    existing_like = PostLike.objects.filter(
        post=post,
        user=request.user
    )

    if existing_like.exists():
        existing_like.delete()
    else:
        PostLike.objects.get_or_create(
            post=post,
            user=request.user
        )

    return redirect('home')


# COMMENT ON A FOOTBALL POST
@login_required
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    comment_text = request.POST.get('text', '').strip()

    if comment_text and len(comment_text) <= 1000:
        PostComment.objects.create(
            post=post,
            user=request.user,
            text=comment_text
        )

    return redirect('home')


# FOOTBALL FIXTURES AND RESULTS
def fixture_list(request):
    upcoming_fixtures = Fixture.objects.filter(
        status='UPCOMING'
    ).select_related('home_club', 'away_club')

    completed_fixtures = Fixture.objects.filter(
        status='COMPLETED'
    ).select_related('home_club', 'away_club')

    other_fixtures = Fixture.objects.filter(
        status__in=['POSTPONED', 'CANCELLED']
    ).select_related('home_club', 'away_club')

    return render(request, 'players/fixture_list.html', {
        'upcoming_fixtures': upcoming_fixtures,
        'completed_fixtures': completed_fixtures,
        'other_fixtures': other_fixtures,
    })


# PLAYER SEARCH AND DISCOVERY
def player_search(request):
    players = PlayerProfile.objects.filter(
        role='PLAYER'
    ).order_by('full_name')

    search_query = request.GET.get('q', '').strip()

    if search_query:
        players = players.filter(
            full_name__icontains=search_query
        )

    position = request.GET.get('position', '')
    if position:
        players = players.filter(position=position)

    foot = request.GET.get('foot', '')
    if foot:
        players = players.filter(
            preferred_foot__iexact=foot
        )

    min_age = request.GET.get('min_age', '')
    if min_age.isdigit():
        players = players.filter(
            age__gte=int(min_age)
        )

    max_age = request.GET.get('max_age', '')
    if max_age.isdigit():
        players = players.filter(
            age__lte=int(max_age)
        )

    return render(request, 'players/player_search.html', {
        'players': players,
        'search_query': search_query,
        'selected_position': position,
        'selected_foot': foot,
        'min_age': min_age,
        'max_age': max_age,
    })


# CLUB MANAGEMENT
def club_list(request):
    clubs = Club.objects.all().order_by('name')

    return render(request, 'players/club_list.html', {
        'clubs': clubs
    })


def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    members = club.members.all().order_by('full_name')
    players = members.filter(role='PLAYER')
    coaches = members.exclude(role='PLAYER')

    return render(request, 'players/club_detail.html', {
        'club': club,
        'players': players,
        'coaches': coaches,
    })


# PITCH DETAILS
def pitch_detail(request, pitch_id):
    pitch = get_object_or_404(Pitch, id=pitch_id)
    players = pitch.players.all()

    return render(request, 'players/pitch_detail.html', {
        'pitch': pitch,
        'players': players
    })


# PLAYER DETAILS
def player_detail(request, player_id):
    player = get_object_or_404(PlayerProfile, id=player_id)

    return render(request, 'players/player_detail.html', {
        'player': player
    })


# REGISTRATION
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
        form = UserCreationForm()

    return render(request, 'players/register.html', {
        'form': form
    })


# CREATE PROFILE
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

    return render(request, 'players/create_profile.html', {
        'form': form
    })


# EDIT PROFILE
@login_required
def edit_profile(request):
    profile = get_object_or_404(
        PlayerProfile,
        user=request.user
    )

    if request.method == 'POST':
        form = PlayerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect(
                'player_detail',
                player_id=profile.id
            )
    else:
        form = PlayerProfileForm(instance=profile)

    return render(request, 'players/create_profile.html', {
        'form': form,
        'editing': True
    })


# CREATE POST
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

            return redirect(
                'player_detail',
                player_id=request.user.playerprofile.id
            )
    else:
        form = PostForm()

    return render(request, 'players/create_post.html', {
        'form': form
    })


# SECURE LOGOUT
@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

from .models import Referee

class RefereeForm(forms.ModelForm):
    class Meta:
        model = Referee
        fields = ['full_name', 'phone_number', 'level', 'bio', 'profile_photo']


@login_required
def become_referee(request):
    if hasattr(request.user, 'referee'):
        return redirect('home')

    if request.method == 'POST':
        form = RefereeForm(request.POST, request.FILES)
        if form.is_valid():
            referee = form.save(commit=False)
            referee.user = request.user
            referee.save()
            return redirect('home')
    else:
        form = RefereeForm()

    return render(request, 'players/become_referee.html', {'form': form})

    def referee_list(request):
    referees = Referee.objects.all().order_by('full_name')
    return render(request, 'players/referee_list.html', {'referees': referees})