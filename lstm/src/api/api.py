from flask import Blueprint, request, jsonify
import numpy as np
from lstm.lstm import LSTMModel
from lstm.optimizer import Adam
import matplotlib.pyplot as plt
from lstm.model_saver import load_model, model_exists
from numpy.typing import NDArray
from typing import Tuple

train_bp = Blueprint("train", __name__)

features_amount = 1
input_size = 60
output_size = 1
hidden_sizes = [128, 128]
training_epochs = 200
feature_min_value = 30
feature_max_value = 250
model_file_name = "model.sp"


def initialize_model(sequence_length: int) -> LSTMModel:
    optimizer = Adam(learning_rate=0.001)
    return LSTMModel(
        features_amount, hidden_sizes, output_size, sequence_length, optimizer
    )


model = initialize_model(input_size)
if model_exists(model_file_name):
    load_model(model_file_name).apply_to_model(model)
    print(f"Model file {model_file_name} has been loaded.")
else:
    print(f"Model file {model_file_name} not found. Initializing a new model.")


def normalize_data(
    data: NDArray[np.float64], feature_min: float, feature_max: float
) -> NDArray[np.float64]:
    return (data - feature_min) / (feature_max - feature_min + 1e-8)


def denormalize_data(
    data: NDArray[np.float64], feature_min: float, feature_max: float
) -> NDArray[np.float64]:
    return data * (feature_max - feature_min + 1e-8) + feature_min


@train_bp.route("/train", methods=["POST"])
def train():
    input_data = request.get_json()
    print(f"Received training request for {len(input_data)} companies")

    x_trains = []
    y_trains = []
    for company_data in input_data:
        print(f"Company data: {len(company_data)} entries")
        x_data = np.array([float(item) for item in company_data])
        x_data = np.flip(x_data)
        x_data_norm = normalize_data(x_data, feature_min_value, feature_max_value)
        x_data_norm = x_data_norm.reshape(-1)
        x_train, y_train = create_sequences(x_data_norm, input_size, output_size)
        for x_train_value, y_train_value in zip(x_train, y_train):
            x_trains.append(x_train_value)
            y_trains.append(y_train_value)
    print(f"Start training with {len(x_trains)} sequences of data")
    model.train(x_trains, y_trains, epochs=training_epochs)
    print(f"End training")

    return jsonify({"status": "Training completed successfully."})


@train_bp.route("/predict", methods=["POST"])
def predict():
    request_data = request.get_json()
    prediction_offset = request_data["offset"]
    prediction_days_amount = request_data["days"]
    input_data = request_data["data"]
    show_plot = request_data["showPlot"]
    print(f"Received prediction request with: {len(input_data)} time points")

    data_length = len(input_data)
    if data_length < input_size + prediction_offset:
        return jsonify({"error": "Not enough data points for prediction."}), 400

    x_data = np.flip(np.array([float(item) for item in input_data]))
    x_data_norm = normalize_data(x_data, feature_min_value, feature_max_value).reshape(
        -1
    )
    x_train_norm, _ = create_sequences(x_data_norm, input_size, output_size)
    _, y_train = create_sequences(x_data, input_size, output_size)

    input_window = x_train_norm[-prediction_offset]
    y_actual = []
    predictions_norm = []
    for i in range(
        len(y_train) - prediction_days_amount - prediction_offset,
        len(y_train) - prediction_offset,
    ):
        y_actual.append(y_train[i])

    for i in range(prediction_days_amount):
        predicted_output_norm, _ = model.forward(input_window)
        predictions_norm.append(predicted_output_norm[0][0])
        input_window = np.roll(input_window, -1)
        input_window[-1] = predicted_output_norm[0][0]
    predicted_output = denormalize_data(
        np.array(predictions_norm), feature_min_value, feature_max_value
    ).reshape(-1)

    if show_plot:
        plt.plot(y_actual, label="Actual Price")
        plt.plot(predicted_output, label="Predicted Price")
        plt.ylim(ymin=0)
        plt.xlabel("Time")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.title("Prediction vs Actual")
        plt.ylim(bottom=0)
        plt.show()

    return jsonify(
        {
            "status": "Prediction completed successfully.",
            "data": predicted_output.tolist(),
            "averageLoss": feature_max_value * model.best_loss,
        }
    )


def create_sequences(
    data: NDArray[np.float64], sequence_length: int, prediction_steps: int = 1
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    x, y = [], []
    for i in range(len(data) - sequence_length - prediction_steps + 1):
        x.append(data[i : i + sequence_length])
        y.append(data[i + sequence_length : i + sequence_length + prediction_steps])
    return np.array(x), np.array(y)
