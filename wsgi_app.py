from app import app, socketio

# Configura o app para produção
app.config['SERVER_NAME'] = None
app.config['APPLICATION_ROOT'] = '/'

if __name__ == "__main__":
    socketio.run(app)
