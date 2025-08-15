from flask import Blueprint, request, session, current_app
from twilio.twiml.messaging_response import MessagingResponse
import re
import time

twilio_bp = Blueprint('twilio_bp', __name__)

def navigate_menu(menu_tree, path):
    """Navega pela árvore do menu e retorna o nó atual"""
    current = menu_tree
    for p in path:
        if p in current:
            current = current[p]
        else:
            return None
    return current

def format_menu_options(options):
    """Formata as opções do menu em ordem numérica"""
    sorted_options = sorted(options.items(), key=lambda x: [int(n) for n in x[0].split('.')])
    return [f"{k} - {v['text']}" for k, v in sorted_options]

def get_menu_message(menu_tree, current_path):
    """Gera a mensagem do menu com as opções disponíveis"""
    message = []
    
    if not current_path:  # Menu principal
        message.extend([
            "Olá, Seja bem-vindo! Você está no atendimento do grupo São Gabriel, em qual das unidades deseja atendimento. Digite o número da opção desejada abaixo:",
            ""
        ])
        options = {k: v for k, v in menu_tree.items() if '.' not in k}
        message.extend(format_menu_options(options))
    else:
        current_node = navigate_menu(menu_tree, current_path)
        if current_node and isinstance(current_node, dict):
            if 'text' in current_node:
                message.append(current_node['text'])
                message.append("")
            
            # Encontra as opções diretas deste nível
            prefix = current_path[-1] + '.' if current_path else ''
            next_level = {}
            for k, v in menu_tree.items():
                if k.startswith(prefix) and k.count('.') == prefix.count('.') + 1:
                    next_level[k] = v
            
            if next_level:
                message.extend(format_menu_options(next_level))
    
    message.extend([
        "",
        "0 - Voltar ao menu principal"
    ])
    
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
        resp.message(get_menu_message(menu_tree, []))
        return str(resp)
    
    # Processa entrada numérica (navegação do menu)
    if re.match(r'^\d+(?:\.\d+)*$', body):
        new_path = []
        valid_option = False
        
        if not path:  # No menu principal
            if body in menu_tree:
                new_path = [body]
                valid_option = True
        else:
            # Constrói o novo caminho baseado no atual
            current = path[-1]
            next_option = f"{current}.{body}"
            
            # Verifica se a opção existe no menu
            if next_option in menu_tree:
                new_path = path + [next_option]
                valid_option = True
        
        resp = MessagingResponse()
        if valid_option:
            path[:] = new_path  # Atualiza o caminho na sessão
            resp.message(get_menu_message(menu_tree, path))
        else:
            resp.message("Opção inválida. Digite 0 para voltar ao menu principal.")
    else:
        # Mensagem não reconhecida
        resp = MessagingResponse()
        resp.message("Por favor, escolha uma opção do menu digitando o número correspondente.\n\n" + 
                    get_menu_message(menu_tree, path))
    
    # Emite evento SocketIO para o dashboard
    current_app.socketio.emit('newMessage', {
        'conv_id': from_number,
        'from': from_number,
        'body': body,
        'timestamp': int(time.time())
    })
    
    return str(resp)
