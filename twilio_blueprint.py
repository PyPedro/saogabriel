from flask import Blueprint, request, session, current_app
from twilio.twiml.messaging_response import MessagingResponse
import re
import time

twilio_bp = Blueprint('twilio_bp', __name__, url_prefix='')refix='')

def get_menu_message(current_path):
    """Gera a mensagem do menu com as opções disponíveis"""
    
    # Menu principal
    if not current_path:
        return "\n".join([
            "Olá, Seja bem-vindo! Você está no atendimento do grupo São Gabriel, em qual das unidades deseja atendimento. Digite o número da opção desejada abaixo:",
            "",
            "1 Arcoverde",
            "2 Belo Jardim",
            "3 Buíque",
            "4 Caruaru",
            "5 Garanhuns",
            "6 Gravatá",
            "7 Pesqueira",
            "8 Santa Cruz",
            "9 Toritama"
        ])
    
    # Menu de Arcoverde
    if len(current_path) == 1 and current_path[0] == '1':
        return "\n".join([
            "1 Agendamento de consultas/exames",
            "2 Cartão São Gabriel",
            "3 2ª via de boleto",
            "4 Guia Médico",
            "5 Falar com atendente",
            "0 Retornar ao menu principal"
        ])
    
    # Menu de Belo Jardim
    if len(current_path) == 1 and current_path[0] == '2':
        return "\n".join([
            "1 Agendamento de consultas/exames",
            "2 Cartão São Gabriel",
            "3 2ª via de boleto",
            "4 Guia Médico",
            "5 Falar com atendente",
            "0 Retornar ao menu principal"
        ])
    
    # Menu de Buíque
    if len(current_path) == 1 and current_path[0] == '3':
        return "\n".join([
            "1 Falar com atendente",
            "2 Guia Médico",
            "3 Falar com atendente",
            "0 Retornar ao menu principal"
        ])
    
    # Menu de Caruaru
    if len(current_path) == 1 and current_path[0] == '4':
        return "\n".join([
            "1 Clinica São Gabriel",
            "2 Cartão São Gabriel",
            "3 Laboratório",
            "4 Exames Imagens (Rx, Tomografia, Ultrassonografia)",
            "5 Hospital",
            "6 Fisioterapia",
            "7 Remoção (Ambulância)",
            "0 Retornar ao menu principal"
        ])
    
    # Menu de Garanhuns
    if len(current_path) == 1 and current_path[0] == '5':
        return "\n".join([
            "1️⃣ Agendamento de consultas/exames",
            "2️⃣ Cartão São Gabriel",
            "3️⃣ 2ª via de boleto",
            "4️⃣ Guia Médico",
            "5️⃣ Falar com atendente",
            "0️⃣ Retornar ao menu principal"
        ])
    
    # Menu de Gravatá
    if len(current_path) == 1 and current_path[0] == '6':
        return "\n".join([
            "1️⃣ Agendamento de consultas/exames",
            "2️⃣ Cartão São Gabriel",
            "3️⃣ 2ª via de boleto",
            "4️⃣ Guia Médico",
            "5️⃣ Falar com atendente",
            "0️⃣ Retornar ao menu principal"
        ])
    
    # Menu de Pesqueira
    if len(current_path) == 1 and current_path[0] == '7':
        return "\n".join([
            "1️⃣ Agendamento de consultas/exames",
            "2️⃣ Cartão São Gabriel",
            "3️⃣ 2ª via de boleto",
            "4️⃣ Guia Médico",
            "5️⃣ Falar com atendente",
            "0️⃣ Retornar ao menu principal"
        ])
    
    # Menu de Santa Cruz
    if len(current_path) == 1 and current_path[0] == '8':
        return "\n".join([
            "1️⃣ Agendamento de consultas/exames",
            "2️⃣ Cartão São Gabriel",
            "3️⃣ 2ª via de boleto",
            "4️⃣ Guia Médico",
            "5️⃣ Falar com atendente",
            "0️⃣ Retornar ao menu principal"
        ])
    
    # Menu de Toritama
    if len(current_path) == 1 and current_path[0] == '9':
        return "\n".join([
            "1️⃣ Agendamento de consultas/exames",
            "2️⃣ Cartão São Gabriel",
            "3️⃣ 2ª via de boleto",
            "4️⃣ Guia Médico",
            "5️⃣ Falar com atendente",
            "0️⃣ Retornar ao menu principal"
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
    if body.lower() in ['menu', 'start', 'iniciar']:
        path.clear()
        resp = MessagingResponse()
        resp.message(get_menu_message([]))
        return str(resp)
    
    # Retorna ao menu anterior
    if body == '0' or body.lower() == 'voltar':
        if path:
            path.pop()  # Remove o último nível do caminho
            resp = MessagingResponse()
            if not path:
                resp.message(get_menu_message([]))  # Volta ao menu principal
            else:
                resp.message(get_menu_message(path))  # Mostra menu atual
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
        # Submenus de Caruaru
        if path == ['4']:
            if option == '1':  # Clínica São Gabriel
                path.append(option)  # Adiciona a opção ao caminho
                menu = [
                    "1-Agendamento de Consultas",
                    "2-Agendamento de Consultas (Dr Oscar Barreto)",
                    "3-Endoscopia e Colonoscopia",
                    "4-Resultado de Exames",
                    "5-Falar com Atendente",
                    "0-Retornar ao menu anterior"
                ]
                return str(MessagingResponse().message("\n".join(menu)))
            elif option == '2':  # Cartão São Gabriel
                path.append(option)
                return str(MessagingResponse().message("\n".join([
                    "1️⃣ Faça seu cartão",
                    "2️⃣ 2ª via de Boleto",
                    "3️⃣ Guia Médico",
                    "4️⃣ Orçamento / Consultar valores",
                    "5️⃣ Meu IRPF",
                    "6️⃣ Credenciamento Médico",
                    "0️⃣ Retornar ao menu anterior"
                ])))
            elif option == '3':  # Laboratório
                path.append(option)
                return str(MessagingResponse().message("\n".join([
                    "1️⃣ Orçamentos com cartão São Gabriel",
                    "2️⃣ Orçamentos Particulares",
                    "3️⃣ Resultados de exames",
                    "4️⃣ Outros",
                    "0️⃣ Retornar ao menu anterior"
                ])))
            elif option == '4':  # Exames Imagens
                path.append(option)
                return str(MessagingResponse().message("\n".join([
                    "1️⃣ Biopsias",
                    "2️⃣ Exames Cardiológicos",
                    "3️⃣ Punções",
                    "4️⃣ Neuromiografia",
                    "5️⃣ Ultrassonografia/RX",
                    "0️⃣ Retornar ao menu anterior"
                ])))
            elif option == '5':  # Hospital
                path.append(option)
                return str(MessagingResponse().message("\n".join([
                    "1️⃣ Recepção",
                    "2️⃣ Marcação de consultas eletivas",
                    "3️⃣ Autorizações de convênios",
                    "4️⃣ Financeiro",
                    "5️⃣ Prontuário DPVAT",
                    "6️⃣ Documentação para reembolso",
                    "7️⃣ Falar com atendente",
                    "0️⃣ Retornar ao menu anterior"
                ])))
            elif option == '6':  # Fisioterapia
                path.append(option)
                return str(MessagingResponse().message("\n".join([
                    "1️⃣ Falar com atendente",
                    "0️⃣ Retornar ao menu anterior"
                ])))
            elif option == '7':  # Remoção (Ambulância)
                path.append(option)
                return str(MessagingResponse().message("\n".join([
                    "1️⃣ Falar com atendente",
                    "0️⃣ Retornar ao menu anterior"
                ])))
        
        # Submenus do nível 2 de Caruaru
        elif len(path) == 2 and path[0] == '4':
            if path[1] == '1':  # Submenu Clínica São Gabriel
                if option in ['1', '2', '3', '4', '5']:
                    return str(MessagingResponse().message("Aguarde, você será atendido em instantes..."))
            elif path[1] == '2':  # Submenu Cartão São Gabriel
                if option == '2':  # 2ª via de Boleto
                    return str(MessagingResponse().message("Para agilizar seu atendimento informe seu CPF ou número do contrato."))
                elif option == '4':  # Orçamento / Consultar valores
                    return str(MessagingResponse().message("Para agilizar seu atendimento envie a requisição médica."))
                elif option == '5':  # Meu IRPF
                    return str(MessagingResponse().message("Para agilizar seu atendimento informe seu CPF ou número do contrato."))
            elif path[1] == '3':  # Submenu Laboratório
                if option == '4':  # Outros
                    path.append(option)
                    return str(MessagingResponse().message("\n".join([
                        "1 Coletas Domiciliares",
                        "2 Solicitação de Urgência nos laudos",
                        "3 Falar com atendente",
                        "0 Retornar ao menu anterior"
                    ])))
            elif path[1] == '5':  # Submenu Hospital
                if option == '1':  # Recepção
                    path.append(option)
                    return str(MessagingResponse().message("\n".join([
                        "1 Clinica médica/ Ortopedia",
                        "2 Exames de imagens (Tomografia/RX)",
                        "3 Exames Laboratoriais",
                        "4 Orçamentos de cirurgias",
                        "5 Cadastro de Guias",
                        "6 Falar com atendente",
                        "0 Retornar ao menu anterior"
                    ])))
                elif option == '2':  # Marcação de consultas eletivas
                    return str(MessagingResponse().message("Para agilizar seu atendimento, por favor, informe seu nome completo."))
                elif option == '3':  # Autorizações de convênios
                    path.append(option)
                    return str(MessagingResponse().message("\n".join([
                        "1 Cirurgias",
                        "2 Infiltrações",
                        "3 Falar com atendente",
                        "0 Retornar ao menu anterior"
                    ])))
                elif option == '4':  # Financeiro
                    path.append(option)
                    return str(MessagingResponse().message("\n".join([
                        "1 Valores de contas à pagar",
                        "2 Nota Fiscal (Meu IRPF)",
                        "3 Valores de Procedimentos",
                        "4 Falar com Atendente",
                        "0 Retornar ao menu anterior"
                    ])))
                elif option == '5':  # Prontuário DPVAT
                    return str(MessagingResponse().message("\n".join([
                        "Receber documento de solicitação de Prontuário Médico",
                        "Clique no link para baixar o arquivo: https://bitily.me/MazFH"
                    ])))
                elif option == '6':  # Documentação para reembolso
                    return str(MessagingResponse().message("\n".join([
                        "Receber documento de solicitação de Prontuário Médico",
                        "Clique no link para baixar o arquivo: https://bitily.me/MazFH"
                    ])))
        
        # Submenus do nível 3 de Caruaru
        elif len(path) == 3 and path[0] == '4':
            if path[1] == '5' and path[2] == '3':  # Hospital -> Autorizações de convênios
                if option in ['1', '2']:  # Cirurgias ou Infiltrações
                    return str(MessagingResponse().message("Para agilizar seu atendimento, por favor, informe seu nome completo, o convênio e o nome do médico solicitante."))
    
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
