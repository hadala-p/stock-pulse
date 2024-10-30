from flask import Blueprint, request, jsonify
import numpy as np
from lstm.lstm import LSTMModel
from lstm.optimizer import Adam

train_bp = Blueprint('train', __name__)

# Parametry modelu
input_size = 1
hidden_size = 50
output_size = 1

def initialize_model(sequence_length):
    optimizer = Adam(learning_rate=0.001)
    return LSTMModel(input_size, hidden_size, output_size, sequence_length, optimizer)

@train_bp.route('/train', methods=['POST'])
def train():
    input_data = request.get_json()

    if not input_data or 'data' not in input_data:
        return jsonify({"error": "Invalid input data."}), 400

    data_length = len(input_data['data'])
    if data_length < 10:
        return jsonify({"error": "Not enough data points for training."}), 400

    sequence_length = max(1, int(data_length * 0.8))

    model = initialize_model(sequence_length)

    x_data = np.array([[item['y']] for item in input_data['data']])
    x_train, y_train = [], []

    for i in range(sequence_length, data_length):
        x_train.append(x_data[i-sequence_length:i])
        y_train.append(x_data[i])

    x_train = np.array(x_train).reshape(-1, sequence_length, 1)
    y_train = np.array(y_train).reshape(-1, 1, 1)
    x_train_list = [x_train[i] for i in range(len(x_train))]
    y_train_list = [y_train[i] for i in range(len(y_train))]

    # Trenowanie modelu
    model.train(x_train_list, y_train_list, epochs=10)

    return jsonify({"status": "Training completed successfully."})
