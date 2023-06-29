from flask_sqlalchemy import SQLAlchemy

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
    
    @property
    def full_name(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    