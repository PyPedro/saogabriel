from flask import Flask
from twilio_blueprint import twilio_bp

app = Flask(__name__)
app.register_blueprint(twilio_bp)
