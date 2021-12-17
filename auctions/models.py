
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
    photo_url = models.URLField()
    category = models.ManyToManyField(Category, blank=True, related_name="Listings")


    def __str__(self):
        return self.title



