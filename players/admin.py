from django.contrib import admin
from .models import (
    Pitch,
    PlayerProfile,
    Post,
    Club,
    Fixture,
    Referee,
    PostLike,
    PostComment,
    Tournament,
    Squad,
    SiteSettings,
)


@admin.register(Pitch)
class PitchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'club')
    list_filter = ('club', 'location')
    search_fields = ('name', 'location', 'club__name')
    list_select_related = ('club',)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name', 'location')

from .models import MatchEvent

@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    list_display = ('fixture', 'player', 'event_type', 'minute')
    list_filter = ('event_type', 'fixture')
    search_fields = ('player__full_name',)

    
admin.site.register(PlayerProfile)
admin.site.register(Post)
admin.site.register(Fixture)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(Referee)
admin.site.register(Tournament)
admin.site.register(Squad)
admin.site.register(SiteSettings)