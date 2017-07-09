from . import mongo

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


class User(Resource):
    collection = mongo.db.Users

    def __init__(self, document):
        self.document = document

    @classmethod
    def add(cls, username=None, **kwargs):
        pass

    @classmethod
    def get(cls, username=None, email=None):
        return User(cls.collection.find_one({'username': username}))

    @classmethod
    def update(cls, method, **kwargs):
        pass

    @classmethod
    def delete(cls, username, **kwargs):
        pass

class Post(Resource):
    collection = mongo.db.Posts

    def __init__(self, document):
        self.document = document

    @classmethod
    def add(cls, postname=None, **kwargs):
        pass

    @classmethod
    def get(cls, **kwargs):
        pass

    @classmethod
    def update(cls, method, **kwargs):
        pass

    @classmethod
    def delete(cls, **kwargs):
        pass

class Project(Resource):
    collection = mongo.db.Projects

class Comment(Resource):
    collection = mongo.db.Comments

class Tag(Resource):
    collection = mongo.db.Tags

class Metric(Resource):
    collection = mongo.db.Metric