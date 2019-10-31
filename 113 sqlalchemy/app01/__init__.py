from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from app01.views import user


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy1?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(user.user)
    db.init_app(app=app)
    return app
