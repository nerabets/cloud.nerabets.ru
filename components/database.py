from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Import models
from app.modules.auth.models import *
from app.modules.users.models import *