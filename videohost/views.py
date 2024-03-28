from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *


@login_required
def dashboard(request):
    videos = Video.objects.all()
    profiles = Profile.objects.filter(user=request.user)  # берем только профиль юзера, который зашел


    template = 'videohost/dashboard.html'
    content = {
        'videos': videos,
        'profiles': profiles,
        'title': 'Мой канал'
    }

    return render(request, template, content)

def channel_videos(request):
    videos = Video.objects.all()
    profiles = Profile.objects.all()
    template = 'videohost/my_channel_videos.html'
    content = {
        'videos': videos,
        'profiles': profiles,
        'title': 'Мои видео'
    }

    return render(request, template, content)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'videohost/register_done.html', {'new_user': new_user, 'title': 'Регистрация'})
    else:
        user_form = UserRegistrationForm
    return render(request, 'videohost/register.html', {'user_form': user_form, 'title': 'Регистрация'})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    template = 'videohost/edit.html'
    content = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Редактировать канал'
    }
    return render(request, template, content)

def feed(request):

    videos = Video.objects.all()
    profiles = Profile.objects.all()

    # Проверяем, есть ли поисковой запрос в URL
    search_query = request.GET.get('search', None)

    # Фильтруем видео по запросу
    if search_query:
        videos = videos.filter(title__icontains=search_query)

    # система сортировки видео
    sort_option = request.GET.get('sort', None)
    if sort_option == 'newest':
        videos = videos.order_by('-date_load')  # сначала новые
    elif sort_option == 'oldest':
        videos = videos.order_by('date_load')  # сначала старые
    elif sort_option == 'max_views': #
        videos = videos.order_by('-views_count')

    template = 'videohost/feed.html'
    content = {
        'videos': videos,
        'profiles': profiles,
        'title': 'Главная'
    }
    return render(request,  template, content)


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the video and associate it with the current user's profile
            video = form.save(commit=False)
            video.author = request.user.profile  # Assuming you have a one-to-one relationship between User and Profile
            video.save()
            return redirect('dashboard')  # Redirect to a page displaying the list of videos
    else:
        form = VideoUploadForm()

    template = 'videohost/upload_video.html'
    content = {
        'form': form,
        'title': 'Загрузить видео'
    }
    return render(request, template, content)

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comments_model = Comment.objects.all()
    # мы знаем конкретное видео, video.author - автор видео, соответственно этот канал мы ищем в модели и выводим список его подписчиков
    subscription = Subscription.objects.filter(channel=video.author)
    # проверяем является ли пользователь, который отправляет запрос(request.user.profile) подписчиком канала
    if request.user.is_authenticated:
        subscriber = Subscription.objects.filter(channel=video.author, subscriber=request.user.profile)
        ViewHistory.objects.create(user=request.user, video=video)
    else:
        subscriber = Subscription.objects.all()
    profiles = Profile.objects.all()
    video.views_count += 1
    video.save()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.author = request.user.profile
            comment.save()

        del_comment_id = request.POST.get('del_comment_id', None)
        if del_comment_id:
            comment_to_delete = get_object_or_404(Comment, id=del_comment_id)
            comment_to_delete.delete()

        subscribe = request.POST.get('subscribe', None)
        if subscribe == 'sub':
            # Получаем экземпляры профилей для текущего пользователя и автора видео

            subscriber_profile = request.user.profile
            channel = video.author
            # Создаем объект подписки
            subscription = Subscription(subscriber=subscriber_profile, channel=channel)
            subscription.save()

        unsubscribe = request.POST.get('unsubscribe', None)
        if unsubscribe == 'un-sub':
            subscription.filter(channel=video.author, subscriber=request.user.profile).delete()

        return redirect('video_detail', video_id=video_id)
    else:
        form = CommentForm()

    template = 'videohost/video_detail.html'
    content = {
        'video': video,
        'form': form,
        'comments_model': comments_model,
        'subscription': subscription,
        'profiles': profiles,
        'subscriber': subscriber,
        'title': video.title
    }
    return render(request, template, content)


def video_edit(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'POST':
        video_edit_form = VideoEditForm(request.POST, request.FILES, instance=video)
        if video_edit_form.is_valid():
            video_edit_form.save()
            del_video_option = request.POST.get('del', None)
            if del_video_option == 'del_video':
                video.delete()
                return redirect('channel_videos')
    else:
        video_edit_form = VideoEditForm(instance=video)

    template = 'videohost/video_edit.html'
    content = {
        'video_edit_form': video_edit_form,
        'video': video,
        'title': 'Редактировать видео'
        }
    return render(request, template, content)

def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    template = 'videohost/playlist_detail.html'
    content = {
        'playlist': playlist,
        'title': playlist.video.title
    }
    return render(request, template, content)

def my_channel_settings(request):
    profiles = Profile.objects.all()

    template = 'videohost/my_channel_settings.html'
    content = {
        'profiles': profiles,
        'title': 'Настройки канала'
    }
    return render(request, template, content)

@login_required
def views_history(request):
    template = 'videohost/views_history.html'
    history = ViewHistory.objects.filter(user=request.user)
    content = {
        'history': history,
        'title': 'История просмотров'
    }
    return render(request, template, content)

@login_required
def my_subscriptions(request):
    my_subscriptions = Subscription.objects.filter(subscriber=request.user.profile)
    video = Video.objects.all()
    template = 'videohost/my_subscriptions.html'
    content = {
        'my_subscriptions': my_subscriptions,
        'video': video,
        'title': 'Мои подписки'
    }
    return render(request, template, content)
