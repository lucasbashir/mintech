# Generated by Django 4.1.7 on 2023-08-15 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minsocial', '0013_remove_video_viewers_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='viewers_ip',
            field=models.TextField(blank=True),
        ),
    ]
