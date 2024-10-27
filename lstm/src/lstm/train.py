import numpy as np
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
from lstm import LSTMModel
from optimizer import Adam
import matplotlib.pyplot as plt

symbol = 'AAPL'

data = yf.download(symbol, start='2015-01-01', end='2024-05-30')
close_prices = data['Close'].values.reshape(-1, 1)

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler.fit_transform(close_prices)

sequence_length = 60
input_size = 1
hidden_size = 50
output_size = 1
epochs = 10

x_data = []
y_data = []
for i in range(sequence_length, len(scaled_prices)):
    x_data.append(scaled_prices[i-sequence_length:i, 0])
    y_data.append(scaled_prices[i, 0])
x_data, y_data = np.array(x_data), np.array(y_data)

train_size = int(len(x_data) * 0.8)
test_size = len(x_data) - train_size

x_train = x_data[:train_size]
y_train = y_data[:train_size]
x_test = x_data[train_size:]
y_test = y_data[train_size:]

x_train = x_train.reshape(x_train.shape[0], sequence_length, 1)
x_test = x_test.reshape(x_test.shape[0], sequence_length, 1)

optimizer = Adam(learning_rate=0.001)
model = LSTMModel(input_size, hidden_size, output_size, sequence_length, optimizer)

x_train_list = [x_train[i] for i in range(len(x_train))]
y_train_list = [np.array([[y_train[i]]]) for i in range(len(y_train))]
model.train(x_train_list, y_train_list, epochs=epochs)

x_test_list = [x_test[i] for i in range(len(x_test))]
predictions = []
for x in x_test_list:
    prediction = model.predict(x)
    predictions.append(prediction[0][0])

predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

plt.plot(y_test_actual, label='Actual Price')
plt.plot(predictions, label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.legend()
plt.show()
