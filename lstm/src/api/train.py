from flask import Blueprint, request, jsonify
import numpy as np
from lstm.lstm import LSTMModel
from lstm.optimizer import Adam
import matplotlib.pyplot as plt

train_bp = Blueprint('train', __name__)

input_size = 1
hidden_size = 128
output_size = 1
sequence_length = 30
warmup_days = 5

def initialize_model(sequence_length):
    optimizer = Adam(learning_rate=0.001)
    return LSTMModel(input_size, hidden_size, output_size, sequence_length, optimizer)

model = initialize_model(sequence_length)

@train_bp.route('/train', methods=['POST'])
def train():
    input_data = request.get_json()
    print(f"Received data: {len(input_data)} entries")

    data_length = len(input_data)
    if data_length < sequence_length:
        return jsonify({"error": "Not enough data points for training."}), 400  

    x_data = np.array([float(item) for item in input_data])
    x_train, y_train = create_sequences(x_data, sequence_length)
    print(f"Start training")
    model.train(x_train, y_train, epochs=200)
    model.reset_states()
    print(f"End training")

    return jsonify({"status": "Training completed successfully."})


@train_bp.route('/predict', methods=['POST'])
def predict():
    model.reset_states()
    input_data = request.get_json()
    print(f"Received data: {len(input_data)} entries")

    data_length = len(input_data)
    if data_length < sequence_length:
        return jsonify({"error": "Not enough data points for training."}), 400  

    x_data = np.array([float(item) for item in input_data])
    x_train, y_train = create_sequences_old(x_data, sequence_length)

    #warmup
    for i in range(warmup_days):
        predicted_output = model.forward(x_train[i])
        print(f"WARMUP Predicted: {predicted_output[0][0]}, Actual: {y_train[i]}")
    
    predictions = []
    window = x_train[warmup_days]
    y_train_actual = []
    for i in range(0, sequence_length):
        y_train_actual.append(y_train[warmup_days + sequence_length + i])
    days_amount = sequence_length
    for i in range(days_amount):
        predicted_output = model.forward(window)
        predictions.append(predicted_output[0][0])
        window = np.roll(window, -1)
        window[-1] = predicted_output[0][0]

    plt.plot(y_train_actual, label='Actual Price')
    plt.plot(predictions, label='Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()
    return jsonify({"status": "Prediction completed successfully."})

def create_sequences(data, sequence_length):
    x, y = [], []
    i = 0
    while i + sequence_length + 1 < len(data):
        x.append(data[i:i+sequence_length])  # Window of length sequence_length
        y.append(data[i+sequence_length])   # Value at sequence_length + 1
        i += sequence_length + 2            # Move to the next non-overlapping window
    return np.array(x), np.array(y)

def create_sequences_old(data, sequence_length):
    x, y = [], []
    for i in range(len(data) - sequence_length):
        x.append(data[i:i+sequence_length]) 
        y.append(data[i+sequence_length])
    return np.array(x), np.array(y)