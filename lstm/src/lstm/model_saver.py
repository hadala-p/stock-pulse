import pickle


def save_model(model, filename: str):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)


def load_model(filename: str):
    with open(filename, 'rb') as file:
        return pickle.load(file)
