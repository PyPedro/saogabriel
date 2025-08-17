from flask import Blueprint, request, session, current_app
from twilio.twiml.messaging_response import MessagingResponse
import re
import time

twilio_bp = Blueprint('twilio_bp', __name__, url_prefix='')

def get_menu_message(current_path):
    """Gera a mensagem do menu com as opções disponíveis"""
    
    # Menu principal
    if not current_path:
        return "\n".join([
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
    
    # Menu de Arcoverde
    if len(current_path) == 1 and current_path[0] == '1':
        return "\n".join([
            "1-Agendamento de consultas/exames",
            "2-Cartão São Gabriel",
            "3-2ª via de boleto",
            "4-Guia Médico",
            "5-Falar com atendente",
            "0-Retornar ao menu principal"
        ])
    
    # Menu de Belo Jardim
    if len(current_path) == 1 and current_path[0] == '2':
        return "\n".join([
            "1-Agendamento de consultas/exames",
            "2-Cartão São Gabriel",
            "3-2ª via de boleto",
            "4-Guia Médico",
            "5-Falar com atendente",
            "0-Retornar ao menu principal"
        ])
    
    # Menu de Buíque
    if len(current_path) == 1 and current_path[0] == '3':
        return "\n".join([
            "1-Falar com atendente",
            "2-Guia Médico",
            "3-Falar com atendente",
            "0-Retornar ao menu principal"
        ])
    
    # Menu de Caruaru
    if len(current_path) == 1 and current_path[0] == '4':
        return "\n".join([
            "1-Clinica São Gabriel",
            "2-Cartão São Gabriel",
            "3-Laboratório",
            "4-Exames Imagens (Rx, Tomografia, Ultrassonografia)",
            "5-Hospital",
            "6-Fisioterapia",
            "7-Remoção (Ambulância)",
            "0-Retornar ao menu principal"
        ])
    
    # Menu de Garanhuns
    if len(current_path) == 1 and current_path[0] == '5':
        return "\n".join([
            "1-Agendamento de consultas/exames",
            "2-Cartão São Gabriel",
            "3-2ª via de boleto",
            "4-Guia Médico",
            "5-Falar com atendente",
            "0-Retornar ao menu principal"
        ])
    
    # Menu de Gravatá
    if len(current_path) == 1 and current_path[0] == '6':
        return "\n".join([
            "1-Agendamento de consultas/exames",
            "2-Cartão São Gabriel",
            "3-2ª via de boleto",
            "4-Guia Médico",
            "5-Falar com atendente",
            "0-Retornar ao menu principal"
        ])
    
    # Menu de Pesqueira
    if len(current_path) == 1 and current_path[0] == '7':
        return "\n".join([
            "1-Agendamento de consultas/exames",
            "2-Cartão São Gabriel",
            "3-2ª via de boleto",
            "4-Guia Médico",
            "5-Falar com atendente",
            "0-Retornar ao menu principal"
        ])
    
    # Menu de Santa Cruz
    if len(current_path) == 1 and current_path[0] == '8':
        return "\n".join([
            "1-Agendamento de consultas/exames",
            "2-Cartão São Gabriel",
            "3-2ª via de boleto",
            "4-Guia Médico",
            "5-Falar com atendente",
            "0-Retornar ao menu principal"
        ])
    
    # Menu de Toritama
    if len(current_path) == 1 and current_path[0] == '9':
        return "\n".join([
            "1-Agendamento de consultas/exames",
            "2-Cartão São Gabriel",
            "3-2ª via de boleto",
            "4-Guia Médico",
            "5-Falar com atendente",
            "0-Retornar ao menu principal"
        ])
    
    return "Opção inválida. Digite 0 para voltar ao menu principal."

def get_option_by_text(text):
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
    from_number = request.form.get('From', '')
    body = request.form.get('Body', '').strip()
    
    # Inicializa ou obtém a sessão do usuário
    user_session = session.setdefault(from_number, {'path': []})
    path = user_session['path']
    
    # Reinicia navegação se solicitado
    if body.lower() in ['menu', 'start', 'iniciar', 'voltar', '0']:
        path.clear()
        resp = MessagingResponse()
        resp.message(get_menu_message([]))
        return str(resp)
    
    # Processa entrada do usuário (número ou texto)
    option = get_option_by_text(body)
    
    # Se for uma opção válida do menu principal (1-9)
    if re.match(r'^[1-9]$', option):
        path[:] = [option]  # Limpa o caminho e define a nova opção
        resp = MessagingResponse()
        resp.message(get_menu_message(path))
        return str(resp)
    
    # Processa opções dos submenus
    if re.match(r'^\d+$', option) and path:
        # Por enquanto só processa o primeiro nível de submenus
        resp = MessagingResponse()
        resp.message("Em desenvolvimento. Digite 0 para voltar ao menu principal.")
        return str(resp)
    
    # Se chegou aqui, é uma opção inválida
    resp = MessagingResponse()
    if not path:
        resp.message(get_menu_message([]))  # Mostra menu principal
    else:
        resp.message(get_menu_message(path))  # Mostra menu atual
    
    # Emite evento SocketIO para o dashboard
    current_app.socketio.emit('newMessage', {
        'conv_id': from_number,
        'from': from_number,
        'body': body,
        'timestamp': int(time.time())
    })
    
    return str(resp)
