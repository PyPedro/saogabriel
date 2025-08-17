from flask import Blueprint, request, session, current_app
from twilio.twiml.messaging_response import MessagingResponse
import re
import time

twilio_bp = Blueprint('twilio_bp', __name__, url_prefix='')

def get_option_by_text(menu_tree, text):
    """Encontra a opção do menu pelo texto ou número"""
    text = text.lower().strip()
    
    # Mapeamento de textos para números
    text_to_number = {
        'arcoverde': '1',
        'belo jardim': '2',
        'buíque': '3',
        'caruaru': '4',
        'garanhuns': '5',
        'gravatá': '6',
        'pesqueira': '7',
        'santa cruz': '8',
        'toritama': '9'
    }
    
    if text in text_to_number:
        return text_to_number[text]
    return text

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
    return [f"{k}-{v['text']}" for k, v in sorted_options]

def get_menu_message(menu_tree, current_path):
    """Gera a mensagem do menu com as opções disponíveis"""
    message = []
    
    if not current_path:  # Menu principal
        message.extend([
            "Olá, Seja bem-vindo! Você está no atendimento do grupo São Gabriel, em qual das unidades deseja atendimento. Digite o número da opção desejada abaixo:",
            "",
            "1-Arcoverde",
            "2-Belo Jardim",
            "3-Buíque",
            "4-Caruaru",
            "5-Garanhuns",
            "6-Gravatá",
            "7-Pesqueira",
            "8-Santa Cruz",
            "9-Toritama"
        ])
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
            
            # Adiciona opção de voltar apenas para submenus
            message.extend([
                "",
                "0 - Voltar ao menu principal"
            ])
    
    return "\n".join(message)

def get_option_by_text(menu_tree, text):
    """Encontra a opção do menu pelo texto ou número"""
    text = text.lower().strip()
    
    # Mapeamento de textos para números
    text_to_number = {
        'arcoverde': '1',
        'belo jardim': '2',
        'buíque': '3',
        'caruaru': '4',
        'garanhuns': '5',
        'gravatá': '6',
        'pesqueira': '7',
        'santa cruz': '8',
        'toritama': '9'
    }
    
    if text in text_to_number:
        return text_to_number[text]
    return text

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
    
    # Processa entrada do usuário (número ou texto)
    option = get_option_by_text(menu_tree, body)
    
    if option == '1':  # Arcoverde
        path[:] = ['1']  # Limpa o caminho e define como Arcoverde
        resp = MessagingResponse()
        resp.message(get_menu_message(menu_tree, path))
        return str(resp)
    
    # Processa outras opções
    if re.match(r'^\d+(?:\.\d+)*$', option):
        if not path:  # No menu principal
            if option in menu_tree:
                path.append(option)
        else:
            # Adiciona a nova opção ao caminho atual
            full_option = f"{path[-1]}.{option}"
            if full_option in menu_tree:
                path.append(full_option)
    
    # Gera resposta
    resp = MessagingResponse()
    resp.message(get_menu_message(menu_tree, path))
    
    # Emite evento SocketIO para o dashboard
    current_app.socketio.emit('newMessage', {
        'conv_id': from_number,
        'from': from_number,
        'body': body,
        'timestamp': int(time.time())
    })
    
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
