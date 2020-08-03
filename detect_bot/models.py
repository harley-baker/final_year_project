from django.db import models
from django.utils import timezone
import datetime


class TwitterUser(models.Model):
    account_id = models.CharField(max_length=200, primary_key=True, unique=True)
    creation_date = models.DateTimeField()
    statuses_count = models.IntegerField()
    follower_count = models.IntegerField()
    friends_count = models.IntegerField()
    favourites_count = models.IntegerField()
    listed_count = models.IntegerField()
    default_profile = models.BooleanField()
    profile_use_background_image = models.BooleanField()
    verified = models.BooleanField()
    screen_name = models.CharField(max_length=50)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=160)
    last_update = models.DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))

    def __str__(self):
        return self.name

    def account_age(self):
        return timezone.now() - self.creation_date

    def tweet_freq(self):
        return self.statuses_count / self.account_age().seconds

    def follower_growth_rate(self):
        return self.follower_count / self.account_age().seconds

    def friend_growth_rate(self):
        return self.friends_count / self.account_age().seconds

    def favourites_growth_rate(self):
        return self.favourites_count / self.account_age().seconds

    def listed_growth_rate(self):
        return self.listed_count / self.account_age().seconds

    def followers_friends_ratio(self):
        return self.follower_count / self.friends_count if self.friends_count > 0 else 0

    def screen_name_length(self):
        return len(self.screen_name)

    def num_digits_in_screen_name(self):
        return sum(c.isdigit() for c in self.screen_name)

    def name_length(self):
        return len(self.name)

    def num_digits_in_name(self):
        return sum(c.isdigit() for c in self.name)

    def description_length(self):
        return len(self.description) if self.description else 0


class Search(models.Model):
    twitter_user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    classification = models.FloatField()
    search_time = models.DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
