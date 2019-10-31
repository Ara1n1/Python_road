# 1. 选择数据库

from sqlalchemy.engine import create_engine

engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/sqlalchemy?charset=utf8')
from sqlalchemy_study import engine

# 2. 选择表
# 3. 创建查询窗口
from sqlalchemy.orm import sessionmaker

# 选中数据库
select_db = sessionmaker(engine)
# 已经打开查询窗口
db_session = select_db()

"""增加"""

# user = User(name='test', age=18)
# db_session.add(user)
# db_session.commit()
# db_session.close()

"""批量增加"""
# user = [User(name=i) for i in ['dean', 'iris']]
# db_session.add_all(user)
# db_session.commit()
# db_session.close()

"""查询"""

# res = db_session.query(User).all()
# for i in res:
#     print(i.id, i.name)
# db_session.close()

# res = db_session.query(User).filter(User.name == 'dean').first()
# print(res.id, res.name)

# res = db_session.query(User).filter(User.id == 3, User.name == '123').all()
# res = db_session.query(User).filter(True).all()
# res = db_session.query(User).filter(User.id == 1).update({'name': 'henry123'})
# res = db_session.query(User).filter(User.id == 1).first()
# res = db_session.query(User).filter(User.id == 1).delete()
# db_session.commit()
# db_session.close()
# print(res)


# res = db_session.query(User, User.name).count()
# print(res)
# for i in res:
#     print(i.name)


# # sql = "select * from user"
# sql = "insert into user(name, age) values('iris', 18);"
# res = db_session.execute(sql)
# print(res)

"""执行原生SQL"""
# from sqlalchemy import create_engine
#
# db = create_engine('mysql+pymysql://root:root@localhost:3306/sqlalchemy?charset=utf8')
# conn = db.connect()
# # conn.execute("insert into user(name, age) values('iris', 18)")
# res = conn.execute('select * from user')
# # print(list(res))
# print(list(res))