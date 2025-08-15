import re

def parse_fluxo(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    menu = {}
    current_section = None
    num_re = re.compile(r'^(\d+(?:\.\d+)*)\s*-\s*(.+)$')
    
    for line in lines:
        m = num_re.match(line)
        if not m:
            # Se não é uma opção numerada, pode ser texto adicional para a seção atual
            if current_section and current_section in menu:
                menu[current_section]['text'] = menu[current_section]['text'] + "\n" + line
            continue
        
        key, text = m.group(1), m.group(2)
        current_section = key
        
        # Cria a entrada no menu
        menu[key] = {
            'text': text,
            'level': key.count('.'),
            'parent': '.'.join(key.split('.')[:-1]) if '.' in key else None
        }
    
    # Segunda passagem para estabelecer as relações pai-filho
    for key in menu:
        node = menu[key]
        if node['parent'] and node['parent'] in menu:
            parent = menu[node['parent']]
            if 'options' not in parent:
                parent['options'] = {}
            parent['options'][key] = node
    
    return menu
