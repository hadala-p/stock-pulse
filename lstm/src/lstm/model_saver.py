import pickle
import os

def save_model(model, filename: str):
    filename = f"src/{filename}"
    full_path = os.path.abspath(filename)
    with open(full_path, "wb") as file:
        pickle.dump(model, file)


def load_model(filename: str):
    filename = f"src/{filename}"
    full_path = os.path.abspath(filename)
    with open(full_path, "rb") as file:
        return pickle.load(file)


def model_exists(filename: str):
    filename = f"src/{filename}"
    full_path = os.path.abspath(filename)
    print(f"MATI: Checking at path {full_path}")
    try:
        with open(full_path, "rb") as file:
            return True
    except FileNotFoundError:
        return False
