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
    MatchEvent,
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


@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    list_display = (
        'fixture',
        'player',
        'event_type',
        'assisted_by',
        'minute',
    )

    list_filter = ('event_type', 'fixture')

    search_fields = (
        'player__full_name',
        'assisted_by__full_name',
        'fixture__home_club__name',
        'fixture__away_club__name',
    )

    list_select_related = (
        'fixture',
        'player',
        'assisted_by',
    )

    fields = (
        'fixture',
        'event_type',
        'player',
        'assisted_by',
        'minute',
    )


admin.site.register(PlayerProfile)
admin.site.register(Post)
admin.site.register(Fixture)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(Referee)
admin.site.register(Tournament)
admin.site.register(Squad)
admin.site.register(SiteSettings)