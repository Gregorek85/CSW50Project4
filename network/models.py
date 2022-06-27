from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followed_by = models.ManyToManyField(
        "self", related_name="follows", symmetrical=False, default=None, blank=True
    )

    @property
    def number_of_posts(self):
        return self.posts.count()

    @property
    def no_of_following(self):
        return self.follows.count()

    @property
    def number_of_followers(self):
        return self.followed_by.count()


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    content = models.TextField()
    liked_by = models.ManyToManyField(User, related_name="likes", blank=True)
    # AutoFields:
    publication_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)
