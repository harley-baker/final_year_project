from django.shortcuts import render
from utils.twitter import get_user
from utils.data import data_to_list, parse_json_to_data
from utils.neural_net import model_predict


def index(request):
    context = {}
    return render(request, 'index.html', context)


def analyse(request):
    user = get_user(request.POST['accountURL'])
    user_data_row = data_to_list(parse_json_to_data(user, False), user.id, '')[1:-1]
    classification = model_predict('models/drop_off_early_stop.h5', user_data_row)
    prediction = 'Human' if classification > 0.5 else 'Bot'
    confidence = (classification - 0.5) * 200 if classification > 0.5 else (0.5 - classification) * 200
    confidence = round(confidence, 2)
    context = {
        'prediction': prediction,
        'account_name': user.name,
        'classification': classification,
        'confidence': confidence
    }
    return render(request, 'analyse.html', context)


