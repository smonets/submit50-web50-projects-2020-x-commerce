
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.IntegerField()
    photo_url = models.URLField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watch_listings")
    active = models.BooleanField(default=True)
    highest = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.owner}: {self.text}..."

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.IntegerField()

    class Meta:
        verbose_name_plural = "Bids"

    def __str__(self):
        return f"{self.owner}: {self.listing} - {self.bid} $"








