# Generated by Django 4.1.7 on 2023-08-13 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minsocial', '0008_announcementpostimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='announcement_image',
        ),
    ]
