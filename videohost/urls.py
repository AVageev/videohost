from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

from .views import *
from videoru import settings

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('', feed, name='feed'),
    path('upload/', upload_video, name='upload_video'),
    path('video/<int:video_id>/', video_detail, name='video_detail'),
    path('video_edit/<int:video_id>/', video_edit, name='video_edit'),
    path('playlist/<int:playlist_id>/', playlist_detail, name='playlist_detail'),
    path('my_channel_videos/', channel_videos, name='channel_videos'),
    path('my_channel_settings/', my_channel_settings, name='my_channel_settings'),
    path('views_history/', views_history, name='views_history'),
    path('my_subscriptions/', my_subscriptions, name='my_subscriptions'),
    #path('video/<int:video_id>', video, name='video')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)