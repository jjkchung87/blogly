from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

defaultImage = 'https://expertphotography.b-cdn.net/wp-content/uploads/2020/06/stock-photography-trends11.jpg'

"""Models for Blogly."""

class User (db.Model):
    """Site User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                           nullable=False)
    
    last_name = db.Column(db.String(50),
                           nullable=False)
    
    image_URL = db.Column(db.Text,
                           nullable=True,
                           default=defaultImage)

    posts = db.relationship('Post', backref='user', cascade='all, delete')

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_URL}>"

    @property
    def full_name(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    



class Post (db.Model):
    """User posts"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.Text,
                      nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow,
                           server_default=func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # user = db.relationship('User', backref='posts', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Post {self.id} {self.title} {self.content} {self.created_at} {self.user_id}>"