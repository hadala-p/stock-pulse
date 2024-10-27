import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler


def load_data(symbol: str, start: str, end: str, sequence_length: int) -> tuple[np.ndarray, np.ndarray, MinMaxScaler]:
    data = yf.download(symbol, start=start, end=end)
    close_prices = data['Close'].values.reshape(-1, 1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(close_prices)

    x_data, y_data = [], []
    for i in range(sequence_length, len(scaled_prices)):
        x_data.append(scaled_prices[i - sequence_length:i, 0])
        y_data.append(scaled_prices[i, 0])
    return np.array(x_data), np.array(y_data), scaler
