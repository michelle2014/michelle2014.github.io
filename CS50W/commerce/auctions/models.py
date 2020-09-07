from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, Textarea, TextInput
from django.core.files import File
from decimal import Decimal
import urllib
import os


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="users")


class Listing(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True, related_name="listings"
    )
    title = models.CharField(max_length=255)
    starting_price = models.DecimalField(max_digits=9, decimal_places=2)
    current_price = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name="Category",
        null=True,
        blank=True,
    )
    watchlist = models.BooleanField(default=False)
    description = models.TextField()
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=255, null=True, blank=True)
    bid_count = models.DecimalField(
        max_digits=3, decimal_places=0, default=Decimal("0")
    )

    def __str__(self):
        return f"{self.title} bid for ${self.starting_price} created at {self.timestamp} by {self.user} in {self.category}"

    def get_remote_image(self):
        if self.image_url and not self.image:
            result = urllib.urlretrieve(self.image_url)
            self.image.save(os.path.basename(self.image_url), File(open(result[0])))
            self.save()


class Bid(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bids")
    title = models.CharField(max_length=255, default=False)
    bid_price = models.DecimalField(max_digits=9, decimal_places=2)
    bid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.bid_price} bid on {self.title} by {self.user} at {self.bid_at}"


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(max_length=255, default=False)
    text = models.TextField()
    comment_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} commented by {self.user} at {self.comment_at}"


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"


class CreateForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "starting_price",
            "image",
            "image_url",
            "category",
            "description",
        ]
        widgets = {
            "description": Textarea(),
        }


class CreateComment(ModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
        ]
        widgets = {
            "text": Textarea(attrs={"cols": 5, "style": "height: 15em"}),
        }


class CreateBid(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_price"]
        widgets = {
            "bid_price": TextInput(
                attrs={"style": "height: 2.5em", "placeholder": "AU$"}
            )
        }
