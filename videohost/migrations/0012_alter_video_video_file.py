# Generated by Django 4.1.7 on 2024-03-26 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videohost', '0011_subscription_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_file',
            field=models.FileField(blank=True, upload_to='videos/%Y/%m/%d/', verbose_name='Видеофайл'),
        ),
    ]
