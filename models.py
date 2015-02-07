from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

friends = db.Table('friends',
    db.Column('friend_1', db.Integer, db.ForeignKey('users.id')),
    db.Column('friend_2', db.Integer, db.ForeignKey('users.id'))
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    friends = db.relationship('User',
                            secondary=friends,
                            primaryjoin = (friends.c.friend_1 == id),
                            secondaryjoin = (friends.c.friend_2 == id))

    def __init__(self, name):
        self.name = name

    def output(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'friends': [{'name': friend.name, 'id': friend.id} for friend in self.friends]
        }
