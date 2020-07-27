from utils import create_dataset
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)


def generate_data_files():
    create_dataset.parse('datasets/verified-2019/verified-2019.tsv', 'datasets/verified-2019/verified-2019_tweets.json',
                         'humans.csv')
    create_dataset.parse('datasets/celebrity-2019/celebrity-2019.tsv',
                         'datasets/celebrity-2019/celebrity-2019_tweets.json',
                         'humans.csv')
    create_dataset.parse('datasets/creci-rtbust-2019/cresci-rtbust-2019.tsv',
                         'datasets/creci-rtbust-2019/cresci-rtbust-2019_tweets.json',
                         'dataset.csv')
    create_dataset.parse('datasets/midterm-2018/midterm-2018.tsv',
                         'datasets/midterm-2018/midterm-2018_processed_user_objects.json',
                         'dataset.csv')
    create_dataset.parse('datasets/political-bots-2019/political-bots-2019.tsv',
                         'datasets/political-bots-2019/political-bots-2019_tweets.json',
                         'bots.csv')
    create_dataset.parse('datasets/pronbots-2019/pronbots-2019.tsv', 'datasets/pronbots-2019/pronbots-2019_tweets.json',
                         'bots.csv')


def main():
    pass


def train_model(data_file):
    df = read_csv(data_file)
    x, y = df.values[:, 1:-1], df.values[:, -1]
    x = x.astype('float32')
    y = LabelEncoder().fit_transform(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
    print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
    n_features = x_train.shape[1]
    model = Sequential()
    model.add(Dense(10, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
    model.add(Dense(8, activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=150, batch_size=32, verbose=0)
    loss, acc = model.evaluate(x_test, y_test, verbose=0)
    print('Test Accuracy: %.3f' % acc)
    model.save('model.h5')


def model_predict(model_file, account_data):
    model = load_model(model_file)



if __name__ == '__main__':
    main()
