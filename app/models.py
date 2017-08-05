from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Markup, abort
from flask_login import UserMixin
from markdown2 import markdown
from pymongo import ASCENDING, DESCENDING
from . import mongo, login_manager
from manage import app

class Permission:
    COMMENT = 0x02
    MODERATE_COMMENTS = 0x04
    WRITE_ARTICLES = 0x08
    ADMINISTER = 0x80

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
AUTHOR = 'author'
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
            abort(403)
        self.index = document[INDEX]
        self.title = document[TITLE]
        # self.author = document[author]
        self.content = document[CONTENT]
        self.tags = document[TAGS]
        self.added_time = document[ADDED_TIME]
        self.last_modified_time = document[LAST_MODIFIED_TIME]

    def markdown2html(self):
        return Markup(markdown(self.content, extras=['fenced-code-blocks', 'codehilite']))

    def update(self, title=None, content=None, tags=None):
        dic = dict()
        dic[TITLE] = title
        dic[CONTENT] = content
        self.update_tags(self.tags, tags)
        dic[TAGS] = tags
        dic[LAST_MODIFIED_TIME] = datetime.now()
        self.collection.update({INDEX: self.index}, 
                {'$set' : dic})

    def update_tags(self, old, new):
        removed = set(old) - set(new)
        added = set(new) - set(old)

        for tag in removed:
            Tag.remove(tag, self.index)

        for tag in added:
            Tag.add(tag, self.index)

    @property
    def str_added_time(self):
        return self.added_time.strftime('%d %B %Y')

    @classmethod
    def add(cls, title=None, tags=None, content=None, author=None):
        document = dict()
        document[INDEX] = cls.count()   # index starts from 0
        document[TITLE] = title
        document[AUTHOR] = author
        document[CONTENT] = content
        document[TAGS] = tags
        document[ADDED_TIME] = datetime.now()
        document[LAST_MODIFIED_TIME] = document[ADDED_TIME]
        
        # Add tags
        for tag in tags:
            Tag.add(tag, document[INDEX])

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
    def get_all_notes(cls, key=lambda n: n.added_time, reverse=True):
        total_num = Note.count()
        notes = []
        for i in range(total_num):
            notes.append(Note(i))
        notes.sort(key=key, reverse=reverse)
        return notes

    @classmethod
    def get(cls, index):
        return cls.collection.find_one({INDEX: index})

    @classmethod
    def delete(cls, **kwargs):
        pass

    @classmethod
    def count(cls):
        return cls.collection.count()

class Project:
    collection = mongo.db.Projects

class Comment:
    collection = mongo.db.Comments


TAGNAME = 'name'
NOTE_INDEX = 'indexes'
class Tag:
    collection = mongo.db.Tags
    collection.ensure_index(TAGNAME, unique=True)

    def __init__(self, tagname, indexes):
        self.name = tagname
        self.indexes = indexes

    @property
    def notes_cnt(self):
        return len(self.indexes)

    @classmethod
    def get_notes_with_tag(cls, tag):
        document = cls.collection.find_one({TAGNAME: tag})
        if not document or len(document[NOTE_INDEX]) == 0:
            return None
        notes = []
        for index in document[NOTE_INDEX]:
            notes.append(Note(index))
        notes.sort(key=lambda n: n.added_time, reverse=True)
        return notes

    @classmethod
    def add(cls, tagname, note_index):
        if tagname == '':
            return
        document = cls.collection.find_one({TAGNAME: tagname})
        if document:    # Tag exists
            cls.collection.update({TAGNAME: tagname}, 
                    {'$addToSet': {NOTE_INDEX: note_index}})
        else:
            document = {TAGNAME: tagname, NOTE_INDEX: [note_index]}
            cls.collection.insert_one(document)

    @classmethod
    def remove(cls, tagname, note_index):
        document = cls.collection.find_one({TAGNAME: tagname})
        if document:
            cls.collection.update({TAGNAME: tagname}, 
                    {'$pull': {NOTE_INDEX: note_index}})
        else:
            # Should not happen
            pass

    @classmethod
    def get_all_tags(cls):
        tags = []
        for document in cls.collection.find():
            tag = Tag(document[TAGNAME], document[NOTE_INDEX])
            tags.append(tag)
        return tags

class Metric:
    collection = mongo.db.Metric
