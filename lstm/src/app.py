from flask import Flask
from api.api import train_bp

app = Flask(__name__)

app.register_blueprint(train_bp)

if __name__ == '__main__':
    app.run(debug=True)
