from flask import Blueprint, request, jsonify
import numpy as np
from lstm.lstm import LSTMModel
from lstm.optimizer import Adam
import matplotlib.pyplot as plt
from lstm.lstm import LSTMModelData
from lstm.model_saver import load_model, model_exists
from numpy.typing import NDArray

train_bp = Blueprint('train', __name__)

input_size = 1
hidden_sizes = [128, 128]
output_size = 30
sequence_length = 60
epochs = 200
model_file_name = 'model.sp'
selected_sequence = 20

def initialize_model(sequence_length):
    optimizer = Adam(learning_rate=0.0002)
    return LSTMModel(input_size, hidden_sizes, output_size, sequence_length, optimizer)

model = initialize_model(sequence_length)
if model_exists(model_file_name):
    load_model(model_file_name).apply_to_model(model)
    print(f"Model file {model_file_name} has been loaded.")
else:
    print(f"Model file {model_file_name} not found. Initializing a new model.")

def normalize_data(data: NDArray[np.float64], feature_min, feature_max) -> NDArray[np.float64]:
    return (data - feature_min) / (feature_max - feature_min + 1e-8)

def denormalize_data(data: NDArray[np.float64], feature_min, feature_max) -> NDArray[np.float64]:
    return data * (feature_max - feature_min + 1e-8) + feature_min

@train_bp.route('/train', methods=['POST'])
def train():
    input_data = request.get_json()
    print(f"Received data of: {len(input_data)} companies")
    
    x_trains = []
    y_trains = []
    feature_min = float('inf')
    feature_max = -float('inf')
    company_diff_data = []
    for company_data in input_data:
        x_data = np.array([float(item) for item in company_data])
        x_data = np.flip(x_data)
        x_data = np.diff(x_data)
        feature_min = min(feature_min, np.min(x_data))
        feature_max = max(feature_max, np.max(x_data))
        company_diff_data.append(x_data)

    for company_data in company_diff_data:
        print(f"Company data: {len(company_data)} entries")
        x_data_norm = normalize_data(company_data, feature_min, feature_max)
        x_data_norm = x_data_norm.reshape(-1)
        x_train, y_train = create_sequences(x_data_norm, sequence_length, output_size)
        # append x_train elements to x_trains
        # append y_train elements to y_trains
        for x_train_value, y_train_value in zip(x_train, y_train):
            x_trains.append(x_train_value)
            y_trains.append(y_train_value)
    print(f"Start training with {len(x_trains)} sequences of data")
    model.train(x_trains, y_trains, epochs=epochs)
    print(f"End training")

    return jsonify({"status": "Training completed successfully."})


@train_bp.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()
    print(f"Received data: {len(input_data)} entries")

    data_length = len(input_data)
    if data_length < sequence_length:
        return jsonify({"error": "Not enough data points for prediction."}), 400  

    x_data = np.array([float(item) for item in input_data])
    x_data = np.flip(x_data)
    x_data = np.diff(x_data)
    x_train = np.insert(x_data, 0, 0)
    feature_min = np.min(x_train)
    feature_max = np.max(x_train)
    x_data = normalize_data(x_train, feature_min, feature_max)
    x_data = x_data.reshape(-1)
    x_train, y_train = create_sequences(x_data, sequence_length, output_size)

    predicted_output_deltas, _ = model.forward(x_train[selected_sequence])
    predicted_output = np.cumsum(np.insert(predicted_output_deltas.flatten(), 0, x_train[selected_sequence - 1][-1]))

    y_train_actual = y_train[selected_sequence]

    plt.plot(denormalize_data(y_train_actual, feature_min, feature_max).reshape(-1), label='Actual Price')
    plt.plot(denormalize_data(predicted_output, feature_min, feature_max).reshape(-1), label='Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.title("Prediction vs Actual")
    plt.show()

    return jsonify({"status": "Prediction completed successfully."})

def create_sequences(data, sequence_length, prediction_steps = 1):
    x, y = [], []
    for i in range(len(data) - sequence_length - prediction_steps + 1):
        x.append(data[i:i + sequence_length])
        y.append(data[i + sequence_length:i + sequence_length + prediction_steps])
    return np.array(x), np.array(y)
