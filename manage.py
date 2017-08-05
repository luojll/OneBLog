import os

from app import create_app, mongo
from flask_script import Manager, Shell
import Helpers

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

with app.app_context():
    from app.models import User, Note, Tag

def make_shell_context():
    return dict(app=app, mongo=mongo, User=User, Note=Note, Tag=Tag)
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def delete_all_db():
    if app.config['MONGO_DBNAME'] != 'Development':
        raise ValueError("only development db deletes all data")
    User.collection.delete_many({})
    Note.collection.delete_many({})
    Tag.collection.delete_many({})

@manager.command
def add_test_data():
    delete_all_db()
    Helpers.add_test_data(User, Note, Tag)

if __name__ == '__main__':
    manager.run()