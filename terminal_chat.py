import requests
import os
import sys
from datetime import datetime
from colorama import init, Fore, Style

# Inicializa o colorama para funcionar no Windows
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_message(sender, message, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    if sender == "Bot":
        print(f"{Fore.GREEN}[{timestamp}] {sender}:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.BLUE}[{timestamp}] {sender}:{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{message}{Style.RESET_ALL}\n")

def main():
    clear_screen()
    print(f"{Fore.YELLOW}=== Terminal WhatsApp São Gabriel ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Digite 'sair' para encerrar o chat{Style.RESET_ALL}\n")

    # Número do WhatsApp simulado
    phone_number = "whatsapp:+5581999999999"
    
    # URL do webhook (local ou Render)
    webhook_url = "https://saogabriel.onrender.com/whatsapp/webhook"
    
    # Primeira mensagem para iniciar
    response = requests.post(webhook_url, 
                           data={
                               "From": phone_number,
                               "Body": "menu"
                           })
    
    if response.status_code == 200:
        # Extrai a mensagem da resposta TwiML
        from xml.etree import ElementTree
        root = ElementTree.fromstring(response.text)
        message = root.find(".//Message").text
        print_message("Bot", message)
    
    while True:
        try:
            # Recebe entrada do usuário
            user_input = input(f"{Fore.YELLOW}Digite sua mensagem: {Style.RESET_ALL}")
            
            if user_input.lower() == 'sair':
                print(f"\n{Fore.YELLOW}Encerrando chat...{Style.RESET_ALL}")
                break
            
            # Envia a mensagem para o webhook
            print_message("Você", user_input)
            
            response = requests.post(webhook_url,
                                  data={
                                      "From": phone_number,
                                      "Body": user_input
                                  })
            
            if response.status_code == 200:
                # Extrai a mensagem da resposta TwiML
                root = ElementTree.fromstring(response.text)
                message = root.find(".//Message").text
                print_message("Bot", message)
            else:
                print(f"{Fore.RED}Erro ao enviar mensagem. Status code: {response.status_code}{Style.RESET_ALL}")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Encerrando chat...{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Erro: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
