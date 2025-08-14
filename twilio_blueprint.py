from flask import Blueprint, request, session, current_app
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
from flask_socketio import emit
import time
import re

twilio_bp = Blueprint('twilio_bp', __name__)

@twilio_bp.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    menu_tree = current_app.config['MENU_TREE']
    from_number = request.form.get('From')
    body = request.form.get('Body', '').strip().lower()
    conv_id = from_number
    
    # Responde ao "oi" inicial
    if body in ['oi', 'olá', 'ola', 'hello', 'hi']:
        resp = MessagingResponse()
        resp.message("Olá! Bem-vindo ao atendimento automático.\n\n" + 
                    "Escolha uma opção:\n" +
                    "1 - Atendimento\n" +
                    "2 - Horários\n" +
                    "3 - Localização\n" +
                    "4 - Falar com atendente")
        return str(resp)
    sess = session.setdefault(from_number, {'path': [], 'conv_id': conv_id, 'from': from_number})
    path = sess['path']
    # Navegação do menu
    if body.lower() in ['menu', 'start', 'iniciar', 'voltar']:
        path.clear()
    elif re.match(r'\d+(\.\d+)*', body):
        path.append(body)
    # Busca no menu
    node = menu_tree
    for p in path:
        node = next((v for k, v in node.items() if k == p), None)
        if not node:
            path.clear()
            node = menu_tree
            break
        node = node.get('options', {})
    # Mensagem de resposta
    if isinstance(node, dict) and 'text' in node:
        text = node['text']
        options = node.get('options', {})
        if options:
            text += '\n' + '\n'.join([f"{k} - {v['text']}" for k, v in options.items()])
    else:
        text = 'Atendimento encerrado ou opção inválida.'
    # Twilio response
    resp = MessagingResponse()
    resp.message(text)
    # Emite evento SocketIO
    current_app.socketio.emit('newMessage', {
        'conv_id': conv_id,
        'from': from_number,
        'body': body,
        'timestamp': int(time.time())
    })
    return str(resp)
