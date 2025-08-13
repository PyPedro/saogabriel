import os
from flask import Flask, session, send_from_directory
from flask_session import Session
from flask_socketio import SocketIO
from dotenv import load_dotenv
from twilio.rest import Client
from menu_parser import parse_fluxo
from twilio_blueprint import twilio_bp

load_dotenv()

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False, cors_allowed_origins="*")
app.socketio = socketio

menu_tree = parse_fluxo(os.path.join(os.path.dirname(__file__), 'fluxo.txt'))
app.config['MENU_TREE'] = menu_tree

app.register_blueprint(twilio_bp)

# Twilio REST
twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@socketio.on('sendMessage')
def handle_send_message(data):
    conv_id = data.get('conv_id')
    message = data.get('message')
    # Busca número do WhatsApp na sessão
    for k, v in session.items():
        if isinstance(v, dict) and v.get('conv_id') == conv_id:
            to_number = v.get('from')
            break
    else:
        return
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=to_number
    )
    socketio.emit('messageSent', {'conv_id': conv_id, 'body': message})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
