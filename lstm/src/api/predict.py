from flask import Blueprint, request, jsonify
import numpy as np
from lstm.lstm import LSTMModel
from lstm.optimizer import Adam

predict_bp = Blueprint('predict', __name__)

# Parametry modelu
input_size = 1
hidden_size = 50
output_size = 1
sequence_length = 60


def initialize_model() -> LSTMModel:
    optimizer = Adam(learning_rate=0.001)
    return LSTMModel(input_size, hidden_size, output_size, sequence_length, optimizer)


@predict_bp.route('/predict', methods=['POST'])
def predict() -> jsonify:
    input_data = request.get_json()

    # Sprawdzenie poprawności danych wejściowych
    if not input_data or 'data' not in input_data or len(input_data['data']) < sequence_length:
        return jsonify({"error": "Invalid input data or not enough data points for the sequence length."}), 400

    # Inicjalizacja modelu
    model = initialize_model()

    # Przetwarzanie danych wejściowych
    x = np.array([[item['y']] for item in input_data['data'][-sequence_length:]]).reshape(sequence_length, 1)

    # Predykcja
    prediction = model.predict(x)

    # Przygotowanie wyniku do formatu JSON
    output = [{"x": input_data['data'][i]["x"], "y": float(prediction[0][0])} for i in range(len(input_data['data']))]

    return jsonify({"data": output})
