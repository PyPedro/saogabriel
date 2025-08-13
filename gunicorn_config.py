import multiprocessing

bind = "0.0.0.0:$PORT"  # Endereço e porta fornecida pelo Render
worker_class = "eventlet"  # Usando eventlet para suporte a WebSocket
workers = 1  # Número de workers - mantendo 1 para WebSocket
threads = 2  # Número de threads por worker
worker_connections = 1000  # Número máximo de conexões simultâneas
timeout = 30  # Timeout em segundos
keepalive = 2  # Tempo para manter conexões alive

# Configurações de logging
accesslog = "-"  # Log de acesso para stdout
errorlog = "-"   # Log de erro para stderr
loglevel = "info"
