import os
import numpy as np
import matplotlib.pyplot as plt

from pandas import read_csv, concat
from sklearn.preprocessing import MinMaxScaler

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout,BatchNormalization

def test():
    base_path = os.path.join(os.path.abspath(os.getcwd()), 'output', '歷史股價', '上市', '股票', '半導體業', '2330.csv')
    print(base_path)

    df = read_csv(base_path)
    print(df)

    test = df[df.Date>'2021-01-01']
    train = df[:len(df)-len(test)]
    print(test)
    print(train)

    test_set = test['Open']
    train_set = train['Open']
    print(test_set)
    print(train_set)

    sc = MinMaxScaler(feature_range=(0, 1))
    train_set = train_set.values.reshape(-1, 1)
    train_set_scaled = sc.fit_transform(train_set)
    print(train_set)
        
'''
def test():
    base_path = os.path.join(os.path.abspath(os.getcwd()), 'output', '歷史股價', '上市', '股票', '半導體業', '2330.csv')
    
    data = read_csv(base_path)

    print(data)

    test = data[data.Date>'2021-04-01']
    train = data[:len(data)-len(test)]

    train_set = train[['Close', 'Volume']]
    test_set = test[['Close', 'Volume']]

    print(train_set)

    sc = MinMaxScaler(feature_range=(0, 1))
    #需將資料做reshape的動作，使其shape為(資料長度,1) 
    #train_set= train_set.values.reshape(-1,1)
    training_set_scaled = sc.fit_transform(train_set)
    
    X_train = [] 
    y_train = []
    for i in range(10,len(train_set)):
        X_train.append(training_set_scaled[i-10:i-1])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    print(X_train[0])
    print(y_train[0])
    
    keras.backend.clear_session()
    regressor = Sequential()
    regressor.add(LSTM(units = 100, input_shape = (X_train.shape[1], 1)))
    regressor.add(Dense(units = 1))
    regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

    regressor.summary()

    history = regressor.fit(X_train, y_train, epochs=100, batch_size=32)

    dataset_total = concat((train['Close'], test['Close']), axis = 0)
    inputs = dataset_total[len(dataset_total) - len(test) - 10:].values
    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(10, len(inputs)):
        X_test.append(inputs[i-10:i-1, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price = regressor.predict(X_test)
    #使用sc的 inverse_transform將股價轉為歸一化前
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    plt.plot(test['Close'].values, color = 'black', label = 'Real TSMC Stock Price')
    plt.plot(predicted_stock_price, color = 'green', label = 'Predicted TSMC Stock Price')
    plt.title('TATA Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()
    plt.savefig('lstm_2330.png')
    '''