# Generated by Django 3.0.8 on 2020-09-15 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_following_likes_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='default.svg', upload_to='profile_pics/'),
        ),
    ]
