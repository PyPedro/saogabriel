from flask import Blueprint, request, session, current_app
from twilio.twiml.messaging_response import MessagingResponse
import re
import time

twilio_bp = Blueprint('twilio_bp', __name__)

def get_menu_message(menu_node, show_return=True):
    """Gera a mensagem do menu com as opções disponíveis"""
    message = []
    
    if isinstance(menu_node, dict):
        if 'text' in menu_node:
            message.append(menu_node['text'])
        
        options = menu_node.get('options', {})
        if options:
            message.append("\nEscolha uma opção:")
            for key, value in options.items():
                message.append(f"{key} - {value['text']}")
    
    if show_return:
        message.append("\n0 - Voltar ao menu principal")
    
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
        resp.message(get_menu_message(menu_tree))
        return str(resp)
    
    # Processa entrada numérica (navegação do menu)
    if re.match(r'^\d+(?:\.\d+)*$', body):
        # Tenta navegar para a opção selecionada
        current_menu = menu_tree
        temp_path = path.copy()
        temp_path.append(body)
        
        valid_path = True
        final_menu = menu_tree
        
        for step in temp_path:
            if step in current_menu:
                final_menu = current_menu[step]
                current_menu = current_menu[step].get('options', {})
            else:
                valid_path = False
                break
        
        if valid_path:
            path[:] = temp_path  # Atualiza o caminho apenas se for válido
            resp = MessagingResponse()
            resp.message(get_menu_message(final_menu))
        else:
            resp = MessagingResponse()
            resp.message("Opção inválida. Digite 0 para voltar ao menu principal.")
            
    else:
        # Mensagem não reconhecida
        resp = MessagingResponse()
        resp.message("Por favor, escolha uma opção do menu digitando o número correspondente.\n\n" + 
                    get_menu_message(menu_tree))
    
    # Emite evento SocketIO para o dashboard
    current_app.socketio.emit('newMessage', {
        'conv_id': from_number,
        'from': from_number,
        'body': body,
        'timestamp': int(time.time())
    })
    
    return str(resp)
