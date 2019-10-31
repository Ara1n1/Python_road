# 声明一个基类
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

from sqlalchemy import Column, INT, String


# ORM：object relationship mapping
class User(BaseModel):
    # 创建一个table
    __tablename__ = 'user'
    id = Column(INT, primary_key=True, )
    name = Column(String(32), nullable=False, index=True, unique=True)
    age = Column(INT, default=18)

# 数据库引擎创建
from sqlalchemy.engine import create_engine

# 数据库连接驱动语句
engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy?charset=utf8')

# if __name__ == '__main__':
# 利用 User 去数据库创建 user Table
BaseModel.metadata.create_all(engine)
