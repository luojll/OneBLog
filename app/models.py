from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Markup
from flask_login import UserMixin
from markdown import markdown
from pymongo import ASCENDING, DESCENDING
from . import mongo, login_manager
from manage import app

class Permission:
    COMMENT = 0x02
    MODERATE_COMMENTS = 0x04
    WRITE_ARTICLES = 0x08
    ADMINISTER = 0x80

class Resource:

    @classmethod
    def add(cls, **kwargs):
        # Insert a new document to collection
        return NotImplemented()

    @classmethod
    def get(cls, **kwargs):
        # Get a document from collection
        return NotImplemented()

    @classmethod
    def update(cls, **kwargs):
        # Update a document in collection
        return NotImplemented()

    @classmethod
    def delete(cls, **kwargs):
        # Delete a document from collection
        return NotImplemented()

# collection fields for User
USERNAME = 'username'
EMAIL = 'email'
PASSWORD_HASH = 'password_hash'

class User(UserMixin):
    collection = mongo.db.Users
    collection.ensure_index('username', unique=True)
    collection.ensure_index('email', unique=True)

    def __init__(self, **kwargs):
        # super(User, self).__init__(**kwargs)
        document = User.get_user(**kwargs)
        if not document:
            return None
        self.username = document[USERNAME]
        self.email = document[EMAIL]
        self.password_hash = document[PASSWORD_HASH]

    def get_id(self):
        return self.email

    @classmethod
    def is_username_existed(cls, username):
        return User.get_user(username=username) != None

    @classmethod
    def is_email_existed(cls, email):
        return User.get_user(email=email) != None

    @classmethod
    def verify_password(cls, email, password):
        user = User.get_user(email=email)
        return check_password_hash(user[PASSWORD_HASH], password)

    @classmethod
    def add(cls, username=None, email=None, password=None):
        password_hash = generate_password_hash(password)
        cls.collection.insert_one({USERNAME: username, EMAIL: email,
                                    PASSWORD_HASH: password_hash})

    @classmethod
    def get_user(cls, username=None, email=None):
        if username:
            return cls.collection.find_one({USERNAME : username})
        elif email:
            return cls.collection.find_one({EMAIL : email})
        else:
            raise ValueError('Invalid argument')

    @classmethod
    def count(cls):
        return cls.collection.count()

    @classmethod
    def update(cls, method, **kwargs):
        pass

    @classmethod
    def delete(cls, username, **kwargs):
        pass

@login_manager.user_loader
def load_user(email):
    user = User(email=email)
    return user


# collection fields for Note
INDEX = 'id'
TITLE = 'title'
TAGS = 'tags'
CONTENT = 'content'
COMMENT_ID = 'comment_id'
ADDED_TIME = 'added_time'
LAST_MODIFIED_TIME = 'last_modified_time'

class Note:
    collection = mongo.db.Notes
    collection.ensure_index('id', unique=True)

    def __init__(self, index):
        document = Note.get(index)
        if not document:
            return None
        self.index = document[INDEX]
        self.title = document[TITLE]
        self.content = document[CONTENT]
        self.tags = document[TAGS]

    def markdown2html(self):
        return Markup(markdown(self.content))

    @classmethod
    def add(cls, title=None, tags=None, content=None):
        document = dict()
        document[INDEX] = cls.count()   # index starts from 0
        document[TITLE] = title
        document[CONTENT] = content
        document[TAGS] = tags
        document[ADDED_TIME] = datetime.now()
        document[LAST_MODIFIED_TIME] = document[ADDED_TIME]
        cls.collection.insert_one(document)
        return document[INDEX]

    @classmethod
    def get_notes(cls, start_index, show_cnt=app.config['NOTES_PER_PAGE']):
        if start_index > Note.count():
            return None
        notes = []
        i = Note.count() - start_index - 1
        while i >= 0 and show_cnt > 0:
            notes.append(Note(i))
            i, show_cnt = i - 1, show_cnt - 1
        return notes

    @classmethod
    def get(cls, index):
        return cls.collection.find_one({INDEX: index})

    @classmethod
    def update(cls, method, **kwargs):
        pass

    @classmethod
    def delete(cls, **kwargs):
        pass

    @classmethod
    def count(cls):
        return cls.collection.count()

class Project(Resource):
    collection = mongo.db.Projects

class Comment(Resource):
    collection = mongo.db.Comments

class Tag(Resource):
    collection = mongo.db.Tags

class Metric(Resource):
    collection = mongo.db.Metric
