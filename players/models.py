from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from cloudinary.models import CloudinaryField

class Pitch(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, help_text="Area in Wukari")
    description = models.TextField(blank=True)

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
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PLAYER')
    age = models.PositiveIntegerField()
    position = models.CharField(max_length=3, choices=POSITION_CHOICES, default='N/A')
    preferred_foot = models.CharField(max_length=10, blank=True)
    height = models.CharField(max_length=10, blank=True, help_text="e.g. 1.75m")
    bio = models.TextField(blank=True)
    profile_photo = CloudinaryField('image', blank=True, null=True)
    current_pitch = models.ForeignKey(Pitch, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    goals_scored = models.PositiveIntegerField(default=0)
    appearances = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_photo:
            try:
                from PIL import Image, ImageOps
                img = Image.open(self.profile_photo.path)

                # This is the modern and more reliable way to fix orientation
                img = ImageOps.exif_transpose(img)

                # Optional: resize if too large
                if img.height > 800 or img.width > 800:
                    img.thumbnail((800, 800))

                # Save the corrected image
                img.save(self.profile_photo.path)
            except Exception as e:
                print("Error processing image:", e)
class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('PHOTO', 'Photo'),
        ('VIDEO', 'Short Video'),
    ]

    author = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='PHOTO')
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/photos/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.full_name} - {self.get_post_type_display()}"