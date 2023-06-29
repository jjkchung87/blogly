from unittest import TestCase


from app import app
from models import db, User


# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True


# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for view of Users"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()
        user = User(first_name='Rory', last_name='Mcilroy', image_URL='https://b.fssta.com/uploads/application/golf/headshots/380.vresize.350.350.medium.79.png')
        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        """Clean-up fouled transactions"""
        db.session.rollback()

    def testListOfUsers(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Rory', html )
        self.assertIn('Mcilroy', html )

    def testAddNewUser(self):
        with app.test_client() as client:
            d = {'first-name': 'Tiger',
                'last-name' : 'Woods',
                'image-url': 'https://media.cnn.com/api/v1/images/stellar/prod/210223150836-06-tiger-woods-lead-image.jpg?q=w_3000,h_1687,x_0,y_0,c_fill'}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tiger', html)
            self.assertIn('Woods', html)

    def testEditUser(self):
        with app.test_client() as client:
            d = {'first-name': 'Rory',
                'last-name' : 'McDonald',
                'image-url': 'https://media.cnn.com/api/v1/images/stellar/prod/210223150836-06-tiger-woods-lead-image.jpg?q=w_3000,h_1687,x_0,y_0,c_fill'}
            resp = client.post(f'/users/{self.user.id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Rory', html)
            self.assertIn('McDonald', html)

    def testUserDelete(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user.id}/delete',data={}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertNotIn('Rory',html)
            