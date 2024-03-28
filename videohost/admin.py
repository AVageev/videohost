from django.contrib import admin

from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nick', 'name', 'surname', 'age', 'avatar', 'cover', 'about']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview', 'video_file', 'author', 'views_count',
                    'date_load', 'description', 'tags', 'cat']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'video', 'text', 'created_at']

@admin.register(Playlist)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'video', 'creator', 'created_at', 'description', 'access']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'channel']

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'viewed_at']