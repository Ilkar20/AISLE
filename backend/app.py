# backend/app.py
from flask import Flask
from flask_cors import CORS
from config import DEBUG, HOST, PORT
from router import bp as aisle_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(aisle_bp, url_prefix="/api")
    return app

if __name__ == "__main__":
    app = create_app()
    print("Starting AISLE backend on http://%s:%s" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=DEBUG)
