from M2M import Girl, engine, Boy
from sqlalchemy.orm import sessionmaker

select_db = sessionmaker(engine)
db_session = select_db()

# 正向插入数据
# g = Girl(name='echo', gtb=[Boy(name='henry'), Boy(name='henry2')])
# db_session.add(g)
# db_session.commit()
# db_session.close()
#
# res = db_session.query(Girl).all()
# print([(i.name, [j.name for j in i.gtb]) for i in res])

# 反向插入数据

# b = Boy(name='dean')
# b.btg = [Girl(name='iris'), Girl(name='iris2')]
# db_session.add(b)
# db_session.commit()
# db_session.close()

# 反向查询

# res = db_session.query(Boy).all()
# print([(i.name, [j.name for j in i.btg]) for i in res])

# res = db_session.query(Girl).filter(Girl.id == 1).first().gtb
# print(type(res))
# for i in res:
#     print(i.name)

# res = db_session.query(Girl).filter(Girl.id != 1).filter(Girl.id == 2).first()
# print(res.name)

