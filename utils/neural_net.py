from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf

# Have to set these for TF to work on my hardware
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)


def train_model(data_file, output_file, epochs):
    df = read_csv(data_file)
    x, y = df.values[:, 1:-1], df.values[:, -1]
    x = x.astype('float32')
    y = LabelEncoder().fit_transform(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
    print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
    n_features = x_train.shape[1]
    model = Sequential()
    model.add(Dense(100, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
    model.add(Dropout(0.3))
    model.add(Dense(80, activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(30, activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(10, activation='relu', kernel_initializer='he_normal'))
    model.add(Dropout(0.2))
    model.add(Dense(5, activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    early_stop = EarlyStopping(monitor='val_loss', patience=epochs/20.00)
    model.fit(x_train, y_train, epochs=epochs, batch_size=32, verbose=2, validation_split=0.33, callbacks=[early_stop])
    loss, acc = model.evaluate(x_test, y_test, verbose=2)
    print('Test Accuracy: %.3f' % acc)
    model.save(output_file)


def model_predict(model_file, account_data):
    model = load_model(model_file)
    row = [float(i) for i in account_data]
    return model.predict([row])[0][0]
