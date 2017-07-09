import os

from app import create_app, mongo
from flask_script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

with app.app_context():
    from app.models import User, Post, Project, Comment, Tag

def make_shell_context():
    return dict(app=app, mongo=mongo, User=User, Post=Post, Project=Project,
                Comment=Comment, Tag=Tag)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()