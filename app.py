import os
from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO
from flask_cors import CORS
from twilio_blueprint import twilio_bp
from menu_parser import parse_fluxo
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)
Session(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
app.socketio = socketio

# Carrega o menu do arquivo fluxo.txt
menu_tree = parse_fluxo(os.path.join(os.path.dirname(__file__), 'fluxo.txt'))
app.config['MENU_TREE'] = menu_tree

app.register_blueprint(twilio_bp, url_prefix='')

if __name__ == '__main__':
    socketio.run(app, debug=True)
