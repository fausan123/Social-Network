from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    image = models.ImageField(default='default.svg', upload_to='profile_pics/')
    bio = models.TextField(blank=True)


class Posts(models.Model):
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, related_name="posts",
                             on_delete=models.CASCADE)
    post_likes = models.ManyToManyField(
        User, related_name="liked_posts", blank=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.content[:10]}... by {self.user}'


class Likes(models.Model):
    post = models.ForeignKey(
        Posts, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="likes", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post} liked by {self.user}'


class Following(models.Model):
    user = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE)
    follower = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower} follows {self.user}'

    def is_valid_following(self):
        return self.user != self.follower
