from O2O_or_O2M import School, engine, Student
from sqlalchemy.orm import sessionmaker

select_db = sessionmaker(engine)
db_session = select_db()

# 正向插入
# stu = Student(name='iris', stu2sch=School(name='BeiJing'))
# db_session.add(stu)
# db_session.commit()
# db_session.close()

# 反向插入
# sch = School(name='Shanghai')
# sch.sch2stu = [Student(name='henry'), Student(name='echo')]
# db_session.add(sch)
# db_session.commit()
# db_session.close()

# 正向查询
# res = db_session.query(Student).all()
# print([(stu.name, stu.stu2sch.name) for stu in res])

# 反向查询
# res = db_session.query(School).all()
# print([(sch.name, len(sch.sch2stu)) for sch in res])
# print([(sch.name, [stu.name for stu in sch.sch2stu]) for sch in res])
