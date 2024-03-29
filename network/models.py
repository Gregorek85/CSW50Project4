from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, default=None, blank=True
    )

    @property
    def number_of_posts(self):
        return self.posts.count()

    @property
    def no_of_following(self):
        return self.following.count()

    @property
    def number_of_followers(self):
        return self.followed_by.count()


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    content = models.TextField()
    liked_by = models.ManyToManyField(
        User, related_name="likes", blank=True, default=None
    )
    # AutoFields:
    publication_datetime = models.DateTimeField(auto_now_add=True)
    modification_datetime = models.DateTimeField(auto_now=True)

    @property
    def no_of_likes(self):
        return self.liked_by.count()

    class Meta:
        ordering = ["-publication_datetime"]
