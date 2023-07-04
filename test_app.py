from unittest import TestCase


from app import app
from models import db, User, Post, Tag


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
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()
    
        user = User(first_name='Rory', last_name='Mcilroy', image_URL='https://b.fssta.com/uploads/application/golf/headshots/380.vresize.350.350.medium.79.png')
        self.user = user
        golf = Tag(name='Golf')
        self.golf = golf
        sports = Tag(name='Sports')
        self.sports = sports
        tags = [golf, sports]
        post = Post(title='LIV Sucks!', content='You all know the PGA Tour is where it at', user_id=self.user.id )
        post.tags = tags
        self.post = post

        db.session.add_all([user, post])
        db.session.commit()

        


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

    def testPostForm(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user.id}/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="text-center">Add Post for Rory Mcilroy</h1>', html)

    def testNewPostSubmit(self):
        with app.test_client() as client:
            d = {'title':'Greg Norman Sucks',
                 'content':'Nobody likes you. Go away!'}
            resp = client.post(f'/users/{self.user.id}/posts/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Greg Norman Sucks', html)
    
    
    
    def testPostEdit(self):
        with app.test_client() as client:
            d = {'title':'I love the Masters!',
                 'content':'August National is great'}
            resp = client.post(f'/posts/{self.post.id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1 class="text-center">I love the Masters!</h1><br>', html)

    def testPostDelete(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post.id}/delete', data={}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertNotIn('LIV Sucks!',html)
            self.assertIn('<h1 class="text-center">Users</h1>', html)
    
    def testShowTags(self):
        with app.test_client() as client:
            resp = client.get('/tags')
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('>Golf</a></li>',html)
        self.assertIn('>Sports</a></li>',html)

    def testCreateTag(self):
        with app.test_client() as client:
            resp = client.post('/tags/new', data={'tag-name':'Tennis'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('>Tennis</a></li>',html)
        self.assertIn('>Golf</a></li>',html)
        self.assertIn('>Sports</a></li>',html)


    def testEditTag(self):
        with app.test_client() as client:
            resp = client.post(f'/tags/{self.sports.id}/edit', data={'tag-name':'PGA', 'posts':[]}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('>PGA</a></li>', html)
            self.assertNotIn('LIV Sucks!', html)


    def testDeleteTag(self):
        with app.test_client() as client:
            resp=client.post(f'/tags/{self.sports.id}/delete',data={}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('>Golf</a></li>', html)
            self.assertNotIn('Sports', html)
        


