from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

twilio_bp = Blueprint('twilio_bp', __name__)

@twilio_bp.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    # Cria resposta padrão com menu para qualquer mensagem recebida
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
