from unittest import TestCase


from app import app
from models import db, User


# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False


db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for User Model"""

    def setUp(self):
        """clean-up existing users"""

        User.query.delete()

    def tearDown(self):
        """clean up any fouled transactions"""

        db.session.rollback()

    