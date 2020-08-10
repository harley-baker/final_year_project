import tweepy
import json

with open('utils/keys.json') as f:
    data = json.load(f)

CONSUMER_KEY = data['CONSUMER_KEY']
CONSUMER_SECRET = data['CONSUMER_SECRET']
ACCESS_TOKEN = data['ACCESS_TOKEN']
ACCESS_SECRET = data['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def get_user(user):
    return api.get_user(user)