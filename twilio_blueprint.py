from flask import Blueprint, request, session, current_app
from twilio.twiml.messaging_response import MessagingResponse
import re
import time

twilio_bp = Blueprint('twilio_bp', __name__)

@twilio_bp.route('/whatsapp/webhook', methods=['POST'])
def whatsapp_webhook():
    menu_tree = current_app.config['MENU_TREE']
    from_number = request.form.get('From', '')
    body = request.form.get('Body', '').strip()
    
    # Se é uma nova conversa ou pediu para voltar ao menu
    if not session.get(from_number) or body.lower() in ['menu', 'voltar', '0']:
        session[from_number] = {'path': []}
        resp = MessagingResponse()
        menu_text = ("Olá, Seja bem-vindo! Você está no atendimento do grupo São Gabriel, em qual das unidades deseja atendimento. "
                    "Digite o número da opção desejada abaixo:\n\n"
                    "1 - Arcoverde\n"
                    "2 - Belo Jardim\n"
                    "3 - Buíque\n"
                    "4 - Caruaru")
        resp.message(menu_text)
        return str(resp)
    
    # Se escolheu uma opção numérica
    if re.match(r'^\d+(?:\.\d+)*$', body):
        path = session[from_number]['path']
        path.append(body)
        
        # Navega até o nó atual
        current = menu_tree
        for p in path:
            if p not in current:
                path.pop()  # Opção inválida, remove do caminho
                break
            current = current[p].get('options', {})
        
        # Prepara a mensagem de resposta
        resp = MessagingResponse()
        if path:
            node = menu_tree[path[-1]]
            msg = node['text'] + "\n\n"
            options = node.get('options', {})
            if options:
                msg += "Escolha uma opção:\n"
                for k, v in options.items():
                    msg += f"{k} - {v['text']}\n"
            msg += "\n0 - Voltar ao menu principal"
        else:
            msg = "Opção inválida. Digite 0 para voltar ao menu principal."
        
        resp.message(msg)
        return str(resp)
    
    # Para qualquer outra mensagem, mostra o menu principal
    resp = MessagingResponse()
    resp.message("Por favor, escolha uma opção do menu digitando o número correspondente.\n\n"
                "1 - Arcoverde\n"
                "2 - Belo Jardim\n"
                "3 - Buíque\n"
                "4 - Caruaru\n\n"
                "0 - Voltar ao menu principal")
    sess = session.setdefault(from_number, {'path': [], 'conv_id': from_number, 'from': from_number})
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
        'conv_id': from_number,
        'from': from_number,
        'body': body,
        'timestamp': int(time.time())
    })
    return str(resp)
