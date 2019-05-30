from flask_mail import Message

from app import create_app,db,mail
from app.models import User, Role, Post
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand


import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Post=Post)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def send_mail():
    msg = Message('闸种',body="ＮＭＳＬ,WSND\n"
                            "总要有人当five,那为什么不能是我",recipients=["2623387051@qq.com"])
    mail.send(msg)

@manager.command
def fake():
    pass

if __name__ == '__main__':
    manager.run()
