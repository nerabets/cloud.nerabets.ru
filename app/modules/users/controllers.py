from flask import Blueprint
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required)
from flask_restful import (
    Api,
    Resource,)
from components.database import db
from .models import (
    User,
    UserSchema)

module = Blueprint('users', __name__,)
api = Api(module)

# Получить авторизованного пользователя
# /api/v1/user/
class Useritem(Resource):
    @jwt_required()
    def get(self):  
        user = User.query.get(get_jwt_identity())
        return ({"user": UserSchema().dump(user)})

api.add_resource(Useritem, '/')



