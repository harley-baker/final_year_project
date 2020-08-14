from django.shortcuts import render
from django.http import Http404, JsonResponse
from utils.twitter import get_user
from utils.data import data_to_list, parse_json_to_data
from utils.neural_net import model_predict, get_prediction
from .models import TwitterUser, Search
from .UserSearchInfo import UserSearchInfo
from tweepy.error import TweepError
import datetime


def index(request):
    searches = Search.objects.all()
    leaderboard = {}
    for search in searches:
        if search.twitter_user.account_id in leaderboard:
            leaderboard[search.twitter_user.account_id].increment_count()
            leaderboard[search.twitter_user.account_id].prediction = get_prediction(search.classification)
        else:
            leaderboard[search.twitter_user.account_id] = UserSearchInfo(search.twitter_user, 1,
                                                                         get_prediction(search.classification))
    leaderboard = list(leaderboard.values())
    leaderboard.sort(reverse=True, key=lambda i: i.count)
    context = {'leaderboard': leaderboard[:10]}
    return render(request, 'index.html', context)


def analyse(request):
    context = analyse_user(request.POST['username'])
    return render(request, 'analyse.html', context)


def analyse_json(request):
    result = analyse_user(request.GET['username'])
    for i, j in result.items():
        result[i] = str(j)
    return JsonResponse(result)


def analyse_user(username):
    try:
        user = get_user(username)
    except TweepError as e:
        raise Http404(e.reason)
    parsed_user = parse_json_to_data(user, False)
    try:
        user_record = TwitterUser.objects.get(pk=user.id)
        if (datetime.datetime.now(tz=datetime.timezone.utc) - user_record.last_update).days >= 1:
            user_record = create_twitter_user_record(user, parsed_user)
            user_record.save()
    except TwitterUser.DoesNotExist as e:
        user_record = create_twitter_user_record(user, parsed_user)
        user_record.save()
        raise Http404(e)
    user_data_row = data_to_list(parsed_user, user.id, '')[1:-1]
    classification = model_predict('models/no_early.h5', user_data_row)
    prediction = get_prediction(classification)

    confidence = abs((classification - 0.5) * 200)
    confidence = round(confidence, 2)

    search_record = Search(twitter_user=user_record, classification=classification)
    search_record.save()

    return {
        'prediction': prediction,
        'account_name': user.screen_name,
        'classification': classification,
        'confidence': confidence
    }


def create_twitter_user_record(user, parsed_user):
    return TwitterUser(account_id=user.id, creation_date=user.created_at,
                       statuses_count=parsed_user['status_count'],
                       follower_count=parsed_user['follower_count'],
                       friends_count=parsed_user['friends_count'],
                       favourites_count=parsed_user['favourites_count'],
                       listed_count=parsed_user['listed_count'],
                       default_profile=parsed_user['default_profile'],
                       profile_use_background_image=parsed_user['profile_use_background_image'],
                       verified=parsed_user['verified'],
                       screen_name=parsed_user['screen_name'],
                       name=parsed_user['name'],
                       description=parsed_user['description'],
                       last_update=datetime.datetime.now(datetime.timezone.utc))
