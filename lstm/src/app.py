from flask import Flask
from api.train import train_bp
from api.predict import predict_bp

app = Flask(__name__)

app.register_blueprint(train_bp)
app.register_blueprint(predict_bp)

if __name__ == '__main__':
    app.run(debug=True)
