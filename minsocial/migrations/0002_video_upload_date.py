# Generated by Django 4.1.7 on 2023-08-03 00:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('minsocial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
