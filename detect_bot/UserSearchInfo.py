from detect_bot.models import TwitterUser


class UserSearchInfo:
    twitter_user = TwitterUser
    count = 0
    prediction = ''

    def __init__(self, twitter_user, count, prediction):
        self.twitter_user = twitter_user
        self.count = count
        self.prediction = prediction

    def increment_count(self):
        self.count += 1
