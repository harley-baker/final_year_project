# Basic script to run model training
from utils.neural_net import train_model

train_model('parsed_datasets/bots_and_humans.csv', 'models/drop_off_early_stop.h5', 250)
