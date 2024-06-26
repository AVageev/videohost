# Generated by Django 4.1.7 on 2024-03-05 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videohost', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videohost.profile', verbose_name='Автор комментария')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videohost.video', verbose_name='Видео')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='video',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='video_comments', to='videohost.comment', verbose_name='Комментарии'),
        ),
    ]
