from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from time import time
import jwt
from app import db, login
from sqlalchemy_imageattach.entity import Image, image_attachment


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='author')
    ideas = db.relationship('Idea', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class DishType(db.Model):
    __tablename__ = 'dish_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False, unique=True)
    recipes = db.relationship('Recipe', backref='dish_type')

    def __repr__(self):
        return '<DishType {}>'.format(self.name)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    dish_type_id = db.Column(db.Integer, db.ForeignKey('dish_types.id'))
    ingredients = db.relationship('Ingredient', backref='recipe')
    steps = db.relationship('Step', backref='recipe')
    picture = image_attachment('RecipePicture')

    def __repr__(self):
        return '<Recipe {}>'.format(self.title)


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String())


class Step(db.Model):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'), nullable=False)
    content = db.Column(db.String())


class RecipePicture(db.Model, Image):
    __tablename__ = 'pictures'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'), primary_key=True)
    recipe = db.relationship('Recipe')


class Idea(db.Model):
    __tablename__ = 'ideas'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String())
