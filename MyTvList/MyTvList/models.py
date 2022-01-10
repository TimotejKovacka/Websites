from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import tmdbSimpleApi

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='profile_images', blank=True)
    #email_confirmed = models.BooleanField(default=False)
    favourite_show = models.CharField(max_length=150, blank=True)

    #watchlist = [favouriteShow,] removed favouriteShow
    watchlist = []


    def __str__(self):
        return str(self.user.username)

    def add_watchlist(show):
        watchlist.append(tmdbSimpleApi.getId(show))
        
class Review(models.Model):
    review_creator = models.ForeignKey(UserProfile, null = True, on_delete=models.CASCADE)
    showTitle = models.CharField(max_length = 255)
    rating = models.DecimalField(max_digits = 3, decimal_places = 1)
    review = models.CharField(max_length = 496)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)

    def getRating(self):
        return self.Rating
        
    def getReview(self):
        return self.review
        
    def getShowTitle(self):
        return self.showTitle
        
    def getUser(self):
        return self.user.username
