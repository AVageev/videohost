from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    nick = models.CharField(max_length=255, unique=True, verbose_name='Никнейм')
    name = models.CharField(max_length=255, blank=True, verbose_name='Имя')
    surname = models.CharField(max_length=255, blank=True, verbose_name='Фамилия')
    age = models.CharField(max_length=2, blank=True, verbose_name='Возраст')
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, verbose_name='Аватар')
    cover = models.ImageField(upload_to='images/avatar/%Y/%m/%d/', blank=True, verbose_name='Обложка канала')
    about = models.CharField(blank=True, max_length=1000, verbose_name='Описание')


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'
        ordering = ['user']

class Subscription(models.Model):
    subscriber = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Подписчик')
    channel = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscribers', verbose_name='Канал')

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название видео')
    preview = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True, verbose_name='Превью')
    video_file = models.FileField(upload_to='videos/%Y/%m/%d/', blank=True, verbose_name='Видеофайл')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор')
    views_count = models.PositiveIntegerField(verbose_name='Кол-во просмотров', default=0)
    date_load = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    description = models.CharField(max_length=3000, verbose_name='Описание', blank=True)
    comments = models.ManyToManyField('Comment', related_name='video_comments', blank=True, verbose_name='Комментарии')
    playlist = models.ManyToManyField('Playlist', related_name='playlist', blank=True, verbose_name='Плейлист')
    tags = models.CharField(max_length=255, blank=True, verbose_name='Тэги')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ['date_load']


class Category(models.Model):
    category = models.CharField(max_length=100, db_index=True, verbose_name='Категория')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='Видео')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']


class Playlist(models.Model):
    CHOICES = [
        ('Доступно всем', 'Доступно всем'),
        ('Доступно только мне', 'Доступно только мне'),
        ('Доступно по ссылке', 'Доступно по ссылке'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_playlist', verbose_name='Видео')
    creator = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Создатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    access = models.TextField(choices=CHOICES, verbose_name='Права доступа')
    #saved = models.Foreignkey('Profile', on_delete=models.CASCADE, verbose_name='Сохранили')

    class Meta:
        verbose_name = 'Плейлисты'
        verbose_name_plural = 'Плейлисты'
        ordering = ['created_at']

class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'История просмотров'
        verbose_name_plural = 'История просмотров'

