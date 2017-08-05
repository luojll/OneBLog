def add_test_data(User, Note, Tag):
    User.add(username='tester1', email='tester1@test.com', password='test')
    user1 = User(username='tester1')

    User.add(username='tester2', email='tester2@test.com', password='test')
    user2 = User(username='tester2')

    Note.add(title='blog 1', tags=['tag2','tag3','tag1'],
                content='some content', author=user1.username)

    Note.add(title='blog 2', tags=['tag2','tag3','tag4'],
                content='some content', author=user2.username)    
