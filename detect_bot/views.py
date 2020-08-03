from django.shortcuts import render
from utils.twitter import get_user
from utils.data import data_to_list, parse_json_to_data
from utils.neural_net import model_predict
from .models import TwitterUser, Search


def index(request):
    context = {}
    return render(request, 'index.html', context)


def analyse(request):
    user = get_user(request.POST['accountURL'])
    parsed_user = parse_json_to_data(user, False)
    try:
        user_record = TwitterUser.objects.get(pk=user.id)
    except TwitterUser.DoesNotExist:
        user_record = TwitterUser(account_id=user.id, creation_date=user.created_at,
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
                                  description=parsed_user['description'])
        user_record.save()
    user_data_row = data_to_list(parsed_user, user.id, '')[1:-1]
    classification = model_predict('models/drop_off_early_stop.h5', user_data_row)
    prediction = 'Human' if classification > 0.5 else 'Bot'
    confidence = (classification - 0.5) * 200 if classification > 0.5 else (0.5 - classification) * 200
    confidence = round(confidence, 2)

    search_record = Search(twitter_user=user_record, classification=classification)
    search_record.save()

    context = {
        'prediction': prediction,
        'account_name': user.name,
        'classification': classification,
        'confidence': confidence
    }
    return render(request, 'analyse.html', context)
