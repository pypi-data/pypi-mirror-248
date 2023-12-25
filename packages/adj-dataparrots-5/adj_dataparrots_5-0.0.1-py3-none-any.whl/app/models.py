from time import time
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt
import base64
from flask import current_app
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    # user_role：用户角色：管理员：admin、专业用户：professional、普通用户：general
    user_role = db.Column(db.String(128))
    register_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    # might_like：是否开启推荐喜好功能，1：开启、0：关闭，默认开启
    might_like = db.Column(db.Integer, default=1)
    # user_status：1：可用、0：禁用
    user_status = db.Column(db.Integer, default=1)
    is_delete = db.Column(db.Integer, default=0)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def to_dict(self):
        data = {
            'user_id': self.id,
            'username': self.username,
        }
        return data

    def from_dict(self, data, new_user=True):
        self.username = data['username']
        if (new_user == False):
            self.id = data['user_id']

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception as error:
            print(error)
            return

        return User.query.get(id)


class DBConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    db_type = db.Column(db.String(20))
    db_name = db.Column(db.String(32))
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    ip_address = db.Column(db.String(20))
    port_number = db.Column(db.String(10))
    ds_name = db.Column(db.String(32))
    db_summary = db.Column(db.String(1024))
    database_file = db.Column(db.String(1024))
    state = db.Column(db.Integer)
    is_delete = db.Column(db.Integer)
    create_time = db.Column(db.String(30))
    update_time = db.Column(db.String(30))
