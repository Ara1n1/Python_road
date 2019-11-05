from sqlalchemy import func
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from M2M import Girl

engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy?charset=utf8')

db_session = sessionmaker(engine)()

# g1 = Girl(name='diane', gtb=[Boy(name='jack'), Boy(name='jack2')])
# g2 = Girl(name='angle', gtb=[Boy(name='tom'), Boy(name='tom2')])
# db_session.add_all([g1, g2])
# db_session.commit()
# db_session.close()


# res = db_session.query(Girl).filter(Girl.id > 1).filter(Girl.id == 3).first()
# res = db_session.query(Girl).filter_by(name='echo').all()
# print(res[0].name)


# res = db_session.query(Girl).filter(Girl.name != 'echo').all()
# res = db_session.query(Girl).filter(Girl.name == 'echo').all()
# print([i.name for i in res])

query = db_session.query(Girl)

# res = query.filter(Girl.name != 'echo').all()
# print([i.name for i in res])

# # 模糊匹配
# res = query.filter(Girl.name.like('%i%')).all()
# print([i.name for i in res])


# 成员判断

# res = query.filter(~Girl.name.in_(['echo', 'diane', 'haha']))
# print([i.name for i in res])

# None判断

# res = query.filter(Girl.name == None).all()
# res = query.filter(Girl.name != None).all()
# print([i.name for i in res])

# res = query.filter(and_(Girl.name.like('%i%'), Girl.name == 'diane'))
# res = query.filter(Girl.name.like('%i%'), Girl.name == 'diane')
# res = query.filter(Girl.name.like('%i%')).filter( Girl.name == 'diane')
# res = query.filter(or_(Girl.name.like('%i%'), Girl.name == 'diane'))
# print([i.name for i in res])


# res = query.filter().order_by(Girl.id.asc()).all()
# print([(i.id, i.name)for i in res])

# 关联查询
# res = db_session.query(Girl, Boy).filter(Girl.id == Boy.id).all()
# print([[(j.id, j.name) for j in i] for i in res])


# res = db_session.query(Girl).join(Boy).all()
# print([i for i in res])

"""连表查询：表结构在 __init__.py文件中"""

from __init__ import engine, User, Group

db = sessionmaker(engine)()
# u = User(name='echo', utg=Group(name='sale'))
# u2 = User(name='henry', utg=Group(name='tech'))
# u3 = User(name='dean', utg=Group(name='tech'))
# u4 = User(name='iris', utg=Group(name='sale'))
#
# db.add(u2)
# db.add(u3)
# db.add(u4)
#
# db.commit()
# db.close()
# res = db.query(User).all()
# print([i.name for i in res])

# res = db.query(User).join(User.utg).all()
# print([i.name for i in res])

# res = User.join(Group, Group.id == User.g_id).all()
# print([i.name for i in res])

# res = db.query(User, Group).filter(User.g_id == Group.id).all()
# print([[j.name for j in i] for i in res])

# res = db.query(User).join(User.utg).all()
# print([(i.name, i.utg.name) for i in res])


# res = db.query(User, func.count('*')).group_by(User.g_id).all()
# from sqlalchemy import create_engine
# db = create_engine('mysql+pymysql://root:root@localhost:3306/sqlalchemy?charset=utf8')
# conn = db.connect()
# conn.execute("insert into user(name, age) values('haha', 18)")
# res = conn.execute('select * from user')
# print(list(res))