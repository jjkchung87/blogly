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

    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

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

    tags = db.relationship('Tag',secondary='posts_tags', backref='posts')

    postTag = db.relationship('PostTag', backref='posts', cascade='all, delete-orphan')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    # user = db.relationship('User', backref='posts', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Post {self.id} {self.title} {self.content} {self.created_at} {self.user_id}>"
    

class Tag (db.Model):
    """Tags"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                    unique = True )
    
    postTag = db.relationship('PostTag', backref='tags',  cascade='all, delete-orphan')

    def __repr__ (self):
        return f'<Tag {self.id} {self.name}>'


class PostTag (db.Model):
    """Posts and Tags Intersection"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id', ondelete = 'CASCADE'),
                        primary_key=True,
                        nullable=False)
    
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id', ondelete = 'CASCADE'),
                       primary_key=True,
                       nullable=False)
    
    __table_args__ = (
        db.PrimaryKeyConstraint('post_id', 'tag_id'),
    )

