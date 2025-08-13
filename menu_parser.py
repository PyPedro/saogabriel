import re

def parse_fluxo(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    menu = {}
    stack = [(0, menu)]
    num_re = re.compile(r'^(\\d+(?:\\.\\d+)*) - (.+)$')
    for line in lines:
        m = num_re.match(line)
        if not m:
            continue  # ignora linhas sem numeração
        key, text = m.group(1), m.group(2)
        level = key.count('.')
        node = {'text': text, 'options': {}}
        while stack and stack[-1][0] >= level:
            stack.pop()
        if not stack:
            stack = [(0, menu)]  # garante que nunca fique vazio
        stack[-1][1][key] = node
        stack.append((level + 1, node['options']))
    return menu
