# coding: utf-8
from app import create_app, db
from app.auth.models import Role
from app.user.models import User
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Server, Shell, Manager

__author__ = 'Jux.Liu'

app = create_app('default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)

server = Server(host="0.0.0.0", port=5000, use_reloader=True)
manager.add_command("runserver", server)

if __name__ == "__main__":
    manager.run()
