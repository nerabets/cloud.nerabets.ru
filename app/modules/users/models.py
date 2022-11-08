from components.database import db
from components.ma import MA as ma


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(122))
    surname = db.Column(db.String(122))
    email = db.Column(db.String(122), unique=True)
    password = db.Column(db.String(255))

    long_token = db.Column(db.String(300))
    long_token_last_update = db.Column(db.DateTime())
    short_token = db.Column(db.String(300))
    short_token_last_update = db.Column(db.DateTime())

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'email',
                  'long_token_last_update', 'short_token_last_update')

    load_instance = True
    include_fk = True
