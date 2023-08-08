from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return self.categoryName

    class Meta:
        verbose_name_plural = 'Categories'

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="usersBid"
    )

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    starting_bid = models.ForeignKey(
        Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="startingBid"
    )
    image_url = models.URLField()
    isActive = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category"
    )

    def __str__(self):
        return self.title

class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="usersComment"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingsComment"
    )
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"

    class Meta:
        verbose_name_plural = 'Comments'
