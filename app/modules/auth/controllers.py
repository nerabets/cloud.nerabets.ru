from passlib.hash import bcrypt
from datetime import datetime, timedelta, timezone
from flask import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, get_jwt_identity, jwt_required
from flask_restful import (
    Api,
    Resource,
    reqparse,)

from components.jwtmng import jwt_manager
from components.database import db
from .models import TokenBlocklist
from ..users.models import User

module = Blueprint('auth', __name__)
api = Api(module)


@jwt_manager.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

# Проверить авторизован ли пользователь
# /api/v1/auth/
class Protected(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return ({"logged_in_as": current_user}), 200
api.add_resource(Protected, '/')

# Получение токена
# /api/v1/auth/token (POST)
class LoginUserItem(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('password')
        args = parser.parse_args()
        user = User.query.filter(User.email == args['email']).first()
        if user:  # Пользователь с такой почтой есть
            # Проверяем, совпадает ли пароль
            if bcrypt.verify(args['password'], user.password):
                identity = user.id
                access_token = create_access_token(
                    identity, expires_delta=timedelta(seconds=1))
                refresh_token = create_refresh_token(
                    identity, expires_delta=timedelta(days=30))

                user.long_token = refresh_token
                user.short_token = access_token
                user.long_token_last_update = datetime.now(timezone.utc)
                user.short_token_last_update = datetime.now(timezone.utc)

                db.session.add(user)
                db.session.commit()

                return ({
                    "access_token": access_token,
                    "refresh_token": refresh_token
                })
            return ({  # Пароль не подошёл
                "message": "Неверный Email или пароль",
                "errorCode": 1
            }), 401
        return ({  # Пользователя с почтой args['email'] Нет в базе данных
            "message": "Пользователя с такой почтой не существует",
            "errorCode": 2
        }), 401

api.add_resource(LoginUserItem, '/token')

# Обновление токена
# /api/v1/auth/refresh (POST)
class RefreshUserToken(Resource):  # Обновление токена
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(
            identity, expires_delta=timedelta(hours=1))
        user = User.query.get(identity)
        user.short_token = access_token
        user.short_token_last_update = datetime.now(timezone.utc)
        db.session.add(user)
        db.session.commit()
        return ({
            "access_token": access_token
        })

api.add_resource(RefreshUserToken, '/refresh')


# Разлогинить
# /api/v1/auth/loggout (DELETE)
class Loggout(Resource):
    @jwt_required()
    def delete(self):
        identity = get_jwt_identity()
        user = User.query.get(identity)
        jti_short = get_jti(user.short_token)
        jti_long = get_jti(user.long_token)
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti_short, created_at=now))
        db.session.add(TokenBlocklist(jti=jti_long, created_at=now))
        db.session.commit()
        return ({"msg": "JWT revoked"})

api.add_resource(Loggout, '/loggout')


# Регистрация
# /api/v1/auth/register (POST)
class CreateUseritem(Resource):  
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('password')
        args = parser.parse_args()
        user = User.query.filter(User.email == args['email']).first()
        if user:
            return ({
                "message": "Пользователь с такой почтой уже существует",
                "errorCode": "3"
            }), 400
        try:
            user = User(email=args['email'],
                        password=bcrypt.hash(args['password']))
            db.session.add(user)
            db.session.commit()
            return ({
                "message": "Пользователь создан"
            }), 200
        except Exception as e:
            return ({
                "error": e.args
            }), 500

api.add_resource(CreateUseritem, '/register')