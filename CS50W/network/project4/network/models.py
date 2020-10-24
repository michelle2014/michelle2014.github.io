from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


class Follow(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="follows", null=True
    )
    follower = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="followers",
        null=True,
        blank=True,
    )
    following = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="followings",
        null=True,
        blank=True,
    )


class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="liking_users", null=True
    )

    def serialize(self):
        return {
            "id": self.id,
            "post": self.post.id,
            "user": self.user.id,
        }


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "like_count": self.like_count,
        }


class CreatePost(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": Textarea(
                attrs={
                    "placeholder": "What's happening?",
                    "class": "both_postform",
                }
            )
        }
