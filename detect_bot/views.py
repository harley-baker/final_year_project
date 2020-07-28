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
    classification = model_predict('model.h5', user_data_row)
    prediction = 'Human' if classification > 0.5 else 'Bot'
    context = {
        'prediction': prediction,
        'account_name': user.name
    }
    return render(request, 'analyse.html', context)


