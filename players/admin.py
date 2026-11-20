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
        'team',
        'player',
        'event_type',
        'assisted_by',
        'minute',
    )
    list_filter = (
        'event_type',
        'team',
        'fixture',
    )
    search_fields = (
        'player__full_name',
        'assisted_by__full_name',
        'team__name',
        'fixture__home_club__name',
        'fixture__away_club__name',
    )
    list_select_related = (
        'fixture',
        'team',
        'player',
        'assisted_by',
    )
    fields = (
        'fixture',
        'team',
        'event_type',
        'player',
        'assisted_by',
        'minute',
    )


@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    list_display = ('club', 'tournament', 'submitted_at', 'player_count')
    list_filter = ('tournament', 'club')
    search_fields = ('club__name', 'tournament__name')
    filter_horizontal = ('players',)  # Makes adding/removing individual players easy

    def player_count(self, obj):
        return obj.players.count()
    player_count.short_description = 'Players'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "players":
            # When editing an existing squad, show only that club's players
            object_id = request.resolver_match.kwargs.get('object_id') if request.resolver_match else None
            if object_id:
                try:
                    squad = Squad.objects.get(pk=object_id)
                    kwargs['queryset'] = PlayerProfile.objects.filter(
                        club=squad.club,
                        role='PLAYER'
                    ).order_by('full_name')
                except Squad.DoesNotExist:
                    kwargs['queryset'] = PlayerProfile.objects.filter(role='PLAYER').order_by('full_name')
            else:
                # When creating a new squad, show all players (filter after selecting club)
                kwargs['queryset'] = PlayerProfile.objects.filter(role='PLAYER').order_by('full_name')
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(PlayerProfile)
admin.site.register(Post)
admin.site.register(Fixture)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(Referee)
admin.site.register(Tournament)
admin.site.register(SiteSettings)