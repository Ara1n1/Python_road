from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app01 import create_app as create_app1
from app01 import db as db1
from app02 import create_app as create_app2
from app02 import db as db2

"""app01"""
app1 = create_app1()
Migrate(app1, db1)
manager1 = Manager(app1)
manager1.add_command('db1', MigrateCommand)

"""app02"""
app2 = create_app2()
Migrate(app2, db2)
manager2 = Manager(app2)
manager2.add_command('db2', MigrateCommand)


@manager2.command
def func(args):
    print(args)
    return args


@manager2.option('--who', dest='who')
@manager2.option('-a', '--age', dest='age')
def func2(who, age):
    print(who, age)
    return who, age


if __name__ == '__main__':
    manager1.run()
