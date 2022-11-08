import logging
from flask import (Flask)
from flask_cors import CORS
from config import Config
from components.database import db
from components.ma import MA as ma
from components.jwtmng import jwt_manager


def create_app():
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)

    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
    with app.test_request_context():
        db.create_all()
    jwt_manager.init_app(app)
    CORS(app)

    from .modules.auth.controllers import module as auth
    from .modules.users.controllers import module as users

    app.register_blueprint(auth, url_prefix='/api/v1/auth/')
    app.register_blueprint(users, url_prefix='/api/v1/user/')

    return app
