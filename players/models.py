from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField


# FILE UPLOAD SECURITY
def validate_image_upload(file):
    allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
    max_size = 5 * 1024 * 1024  # 5 MB

    extension = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''

    if extension not in allowed_extensions:
        raise ValidationError(
            'Only JPG, JPEG, PNG and WEBP images are allowed.'
        )

    if file.size > max_size:
        raise ValidationError(
            'Image size must not exceed 5 MB.'
        )


def validate_video_upload(file):
    allowed_extensions = ['mp4', 'mov', 'webm']
    max_size = 50 * 1024 * 1024  # 50 MB

    extension = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''

    if extension not in allowed_extensions:
        raise ValidationError(
            'Only MP4, MOV and WEBM videos are allowed.'
        )

    if file.size > max_size:
        raise ValidationError(
            'Video size must not exceed 50 MB.'
        )


class Pitch(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, help_text="Area in Wukari")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    logo = CloudinaryField(
        'image',
        blank=True,
        null=True,
        validators=[validate_image_upload]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PlayerProfile(models.Model):
    ROLE_CHOICES = [
        ('PLAYER', 'Player'),
        ('HEAD_COACH', 'Head Coach'),
        ('ASSISTANT_COACH', 'Assistant Coach'),
        ('GK_COACH', 'Goalkeeper Coach'),
        ('FITNESS_COACH', 'Fitness / Conditioning Coach'),
        ('SCOUT', 'Scout'),
        ('TEAM_MANAGER', 'Team Manager'),
        ('PHYSIO', 'Physiotherapist'),
        ('ANALYST', 'Analyst'),
        ('OTHER', 'Other Staff'),
    ]

    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('FWD', 'Forward/Striker'),
        ('N/A', 'Not Applicable'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='PLAYER'
    )
    age = models.PositiveIntegerField()

    position = models.CharField(
        max_length=3,
        choices=POSITION_CHOICES,
        default='N/A'
    )

    preferred_foot = models.CharField(max_length=10, blank=True)
    height = models.CharField(max_length=10, blank=True, help_text="e.g. 1.75m")
    phone_number = models.CharField(max_length=15, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    state_of_origin = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)

    profile_photo = CloudinaryField(
        'image',
        blank=True,
        null=True,
        validators=[validate_image_upload]
    )

    current_pitch = models.ForeignKey(
        Pitch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='players'
    )

    club = models.ForeignKey(
        Club,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )

    goals_scored = models.PositiveIntegerField(default=0)
    appearances = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('PHOTO', 'Photo'),
        ('VIDEO', 'Short Video'),
    ]

    author = models.ForeignKey(
        PlayerProfile,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES,
        default='PHOTO'
    )

    caption = models.TextField(blank=True)

    image = models.ImageField(
        upload_to='posts/photos/',
        blank=True,
        null=True,
        validators=[validate_image_upload]
    )

    video = models.FileField(
        upload_to='posts/videos/',
        blank=True,
        null=True,
        validators=[validate_video_upload]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.full_name} - {self.get_post_type_display()}"


class Fixture(models.Model):
    STATUS_CHOICES = [
        ('UPCOMING', 'Upcoming'),
        ('COMPLETED', 'Completed'),
        ('POSTPONED', 'Postponed'),
        ('CANCELLED', 'Cancelled'),
    ]

    home_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='home_fixtures'
    )

    away_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        related_name='away_fixtures'
    )

    match_date = models.DateField()
    match_time = models.TimeField()
    venue = models.CharField(max_length=200)

    home_score = models.PositiveIntegerField(null=True, blank=True)
    away_score = models.PositiveIntegerField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='UPCOMING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['match_date', 'match_time']

    def clean(self):
        if self.home_club == self.away_club:
            raise ValidationError(
                "A club cannot play against itself."
            )

    def __str__(self):
        return f"{self.home_club} vs {self.away_club} - {self.match_date}"