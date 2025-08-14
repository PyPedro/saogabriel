import os
from flask import Flask
from flask_session import Session
from twilio_blueprint import twilio_bp
from menu_parser import parse_fluxo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Altere para uma chave secreta real
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Carrega o menu do arquivo fluxo.txt
menu_tree = parse_fluxo(os.path.join(os.path.dirname(__file__), 'fluxo.txt'))
app.config['MENU_TREE'] = menu_tree

app.register_blueprint(twilio_bp)
