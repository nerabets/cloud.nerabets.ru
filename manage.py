from asgiref.wsgi import WsgiToAsgi
from app import create_app

app = create_app()
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    app.run()