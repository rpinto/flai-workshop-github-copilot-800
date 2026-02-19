from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'team_id', 'created_at']
    list_filter = ['team_id', 'created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['_id', 'created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('_id', 'name', 'email')
        }),
        ('Team', {
            'fields': ('team_id',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    readonly_fields = ['_id', 'created_at']
    
    fieldsets = (
        ('Team Information', {
            'fields': ('_id', 'name', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_type', 'user_id', 'duration', 'calories', 'date', 'created_at']
    list_filter = ['activity_type', 'date', 'created_at']
    search_fields = ['user_id', 'activity_type']
    readonly_fields = ['_id', 'created_at']
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('_id', 'user_id', 'activity_type', 'duration', 'calories', 'distance', 'date')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'team_id', 'total_points', 'total_activities', 'total_calories', 'rank', 'updated_at']
    list_filter = ['team_id', 'rank', 'updated_at']
    search_fields = ['user_id', 'team_id']
    readonly_fields = ['_id', 'updated_at']
    ordering = ['-total_points']
    
    fieldsets = (
        ('Leaderboard Information', {
            'fields': ('_id', 'user_id', 'team_id')
        }),
        ('Statistics', {
            'fields': ('total_points', 'total_activities', 'total_calories', 'rank')
        }),
        ('Timestamps', {
            'fields': ('updated_at',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty', 'duration', 'category', 'created_at']
    list_filter = ['difficulty', 'category', 'created_at']
    search_fields = ['name', 'category']
    readonly_fields = ['_id', 'created_at']
    
    fieldsets = (
        ('Workout Information', {
            'fields': ('_id', 'name', 'description', 'difficulty', 'duration', 'category')
        }),
        ('Exercises', {
            'fields': ('exercises',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
