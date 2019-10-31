# db是 sqlalchemy 对象
from app01 import db
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()


# db.Model 就是 BaseModel，使用的是sqlalchemy
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    age = db.Column(db.INT, default=18)


if __name__ == '__main__':
    from app01 import create_app
    app = create_app()
    db.drop_all(app=app)
    db.create_all(app=app)
