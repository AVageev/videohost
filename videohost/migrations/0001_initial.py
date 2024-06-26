# Generated by Django 4.1.7 on 2024-03-01 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(db_index=True, max_length=100, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название видео')),
                ('preview', models.ImageField(blank=True, upload_to='images/%Y/%m/%d/', verbose_name='Превью')),
                ('video_file', models.ImageField(blank=True, upload_to='images/%Y/%m/%d/', verbose_name='Видеофайл')),
                ('author', models.CharField(max_length=255, verbose_name='Автор')),
                ('views_count', models.IntegerField(default=0, verbose_name='Кол-во просмотров')),
                ('date_load', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')),
                ('description', models.CharField(blank=True, max_length=3000, verbose_name='Описание')),
                ('tags', models.CharField(blank=True, max_length=255, verbose_name='Тэги')),
                ('cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='videohost.category')),
            ],
            options={
                'verbose_name': 'Видео',
                'verbose_name_plural': 'Видео',
                'ordering': ['date_load'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick', models.CharField(max_length=255, unique=True, verbose_name='Никнейм')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Имя')),
                ('surname', models.CharField(blank=True, max_length=255, verbose_name='Фамилия')),
                ('age', models.CharField(blank=True, max_length=2, verbose_name='Возраст')),
                ('photo', models.ImageField(blank=True, upload_to='users/%Y/%m/%d/', verbose_name='Фото')),
                ('about', models.CharField(blank=True, max_length=1000, verbose_name='Описание')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профиль',
                'ordering': ['user'],
            },
        ),
    ]
