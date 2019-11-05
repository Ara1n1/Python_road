"""连表查询的model"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

BaseModel = declarative_base()
engine = create_engine('mysql+pymysql://root:root@localhost:3306/sqlalchemy_join?charset=utf8')


class User(BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=True)

    g_id = Column(Integer, ForeignKey('group.id'))
    utg = relationship('Group', backref='gtu')


class Group(BaseModel):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=True)


BaseModel.metadata.create_all(engine)
