# Generated by Django 4.1.7 on 2023-08-13 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('minsocial', '0006_remove_grouppost_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouppostimage',
            name='postContent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_post_images', to='minsocial.grouppost'),
        ),
    ]
