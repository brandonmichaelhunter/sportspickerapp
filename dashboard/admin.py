from django.contrib import admin
from .models import Sport, Team, Game, UserPick


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'sport', 'record']
    list_filter = ['sport']
    search_fields = ['name', 'city']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'location', 'is_completed', 'home_score', 'away_score']
    list_filter = ['sport', 'is_completed', 'game_date']
    search_fields = ['home_team__name', 'away_team__name', 'location']
    date_hierarchy = 'game_date'


@admin.register(UserPick)
class UserPickAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'pick', 'pick_date']
    list_filter = ['pick', 'pick_date']
    search_fields = ['user__username', 'game__home_team__name', 'game__away_team__name']
