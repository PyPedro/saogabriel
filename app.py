from flask import Flask
from twilio_blueprint import twilio_bp

app = Flask(__name__)
app.register_blueprint(twilio_bp)

if __name__ == '__main__':
    app.run()

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
