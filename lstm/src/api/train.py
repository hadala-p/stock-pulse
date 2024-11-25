from flask import Blueprint, request, jsonify
import numpy as np
from lstm.lstm import LSTMModel
from lstm.optimizer import Adam
import matplotlib.pyplot as plt
from lstm.lstm import LSTMModelData
from lstm.model_saver import save_model, load_model, model_exists

train_bp = Blueprint('train', __name__)

input_size = 1
hidden_size = 300
output_size = 30
sequence_length = 30
epochs = 3
model_file_name = 'model.sp'

def initialize_model(sequence_length):
    optimizer = Adam(learning_rate=0.001)
    return LSTMModel(input_size, hidden_size, output_size, sequence_length, optimizer)

model = initialize_model(sequence_length)
if model_exists(model_file_name):
    model_data = load_model(model_file_name)
    model.load_model(model_data)
    print(f"Model file {model_file_name} has been loaded.")
else:
    print(f"Model file {model_file_name} not found. Initializing a new model.")

@train_bp.route('/train', methods=['POST'])
def train():
    input_data = request.get_json()
    print(f"Received data: {len(input_data)} entries")

    data_length = len(input_data)
    if data_length < sequence_length:
        return jsonify({"error": "Not enough data points for training."}), 400  
    
    x_data = np.array([float(item) for item in input_data])
    print(f"Data shape: {x_data.shape}")
    x_data_norm = model.normalize_data(x_data)
    x_data_norm = x_data_norm.reshape(-1)

    x_train, y_train = create_sequences(x_data_norm, sequence_length, output_size)
    print(f"Start training")
    model.train(x_train, y_train, epochs=epochs)
    print(f"End training")

    print(f"Saving model to a file")
    model_data = LSTMModelData(model)
    save_model(model_data, model_file_name)
    print(f"Model saved succesfully")

    return jsonify({"status": "Training completed successfully."})


@train_bp.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()
    print(f"Received data: {len(input_data)} entries")

    data_length = len(input_data)
    if data_length < sequence_length:
        return jsonify({"error": "Not enough data points for prediction."}), 400  

    # Preprocess input data
    x_data = np.array([float(item) for item in input_data])
    x_data = model.normalize_data(x_data)
    x_data = x_data.reshape(-1)
    x_train, y_train = create_sequences(x_data, sequence_length, output_size)

    # Predict for the first sequence in the batch
    predicted_output, _ = model.forward(x_train[0])

    y_train_actual = y_train[0]

    # Plot actual vs. predicted values
    plt.plot(model.denormalize_data(y_train_actual).reshape(-1), label='Actual Price')
    plt.plot(model.denormalize_data(predicted_output).reshape(-1), label='Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.title("Prediction vs Actual")
    plt.show()

    return jsonify({"status": "Prediction completed successfully."})

def create_sequences(data, sequence_length, prediction_steps = 1):
    x, y = [], []
    for i in range(len(data) - sequence_length - prediction_steps + 1):
        x.append(data[i:i + sequence_length])  # Input sequence of length sequence_length
        y.append(data[i + sequence_length:i + sequence_length + prediction_steps])  # Future values (size: prediction_steps)
    return np.array(x), np.array(y)
