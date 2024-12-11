from flask import Flask
from flask_cors import CORS
from api.api import train_bp

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(train_bp)

if __name__ == "__main__":
    app.run(debug=True)
