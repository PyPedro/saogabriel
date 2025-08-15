from flask import Blueprint, request, session, current_app
from twilio.twiml.messaging_response import MessagingResponse
import re
import time

twilio_bp = Blueprint('twilio_bp', __name__)

def get_menu_message(menu_node, show_return=True):
    """Gera a mensagem do menu com as opções disponíveis"""
    message = []
    
    if not menu_node:  # Menu principal
        message.extend([
            "Olá, Seja bem-vindo! Você está no atendimento do grupo São Gabriel, em qual das unidades deseja atendimento. Digite o número da opção desejada abaixo:",
            "",
            "1 - Arcoverde",
            "2 - Belo Jardim",
            "3 - Buíque",
            "4 - Caruaru",
            "5 - Garanhuns",
            "6 - Gravatá",
            "7 - Pesqueira",
            "8 - Santa Cruz",
            "9 - Toritama"
        ])
    elif isinstance(menu_node, dict):
        if 'text' in menu_node:
            message.append(menu_node['text'])
            message.append("")  # Linha em branco para separação
        
        options = menu_node.get('options', {})
        if options:
            for key, value in sorted(options.items()):
                message.append(f"{key} - {value['text']}")
    
    if show_return and len(message) > 0:
        message.append("")  # Linha em branco antes da opção de retorno
        message.append("0 - Voltar ao menu principal")
    
    return "\n".join(message)

@twilio_bp.route('/whatsapp/webhook', methods=['POST'])
def whatsapp_webhook():
    menu_tree = current_app.config['MENU_TREE']
    from_number = request.form.get('From', '')
    body = request.form.get('Body', '').strip()
    
    # Inicializa ou obtém a sessão do usuário
    user_session = session.setdefault(from_number, {'path': []})
    path = user_session['path']
    
    # Reinicia navegação se solicitado
    if body.lower() in ['menu', 'start', 'iniciar', 'voltar', '0']:
        path.clear()
        resp = MessagingResponse()
        resp.message(get_menu_message(None))  # Menu principal
        return str(resp)
    
    # Processa entrada numérica (navegação do menu)
    if re.match(r'^\d+(?:\.\d+)*$', body):
        current_menu = menu_tree
        current_node = None
        
        if not path:  # No menu principal
            if body in menu_tree:
                path.append(body)
                current_node = menu_tree[body]
        else:
            # Navega até o nó atual
            for p in path:
                if p in current_menu:
                    current_menu = current_menu[p].get('options', {})
            
            # Tenta adicionar nova opção ao caminho
            full_option = f"{path[-1]}.{body}" if path else body
            if full_option in menu_tree:
                path.append(full_option)
                current_node = menu_tree[full_option]
            elif body in current_menu:
                path.append(body)
                current_node = current_menu[body]
        
        resp = MessagingResponse()
        if current_node:
            resp.message(get_menu_message(current_node))
        else:
            resp.message("Opção inválida. Digite 0 para voltar ao menu principal.")
    else:
        # Mensagem não reconhecida
        resp = MessagingResponse()
        resp.message("Por favor, escolha uma opção do menu digitando o número correspondente.\n\n" + 
                    get_menu_message(None))  # Menu principal
    
    # Emite evento SocketIO para o dashboard
    current_app.socketio.emit('newMessage', {
        'conv_id': from_number,
        'from': from_number,
        'body': body,
        'timestamp': int(time.time())
    })
    
    return str(resp)
