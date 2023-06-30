"""Blogly application."""
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chickenzarecool21837'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.app_context().push()
connect_db(app)
db.create_all()

@app.route('/')
def show5RecentPosts():
    posts = Post.query.order_by(desc(Post.created_at)).all()
    fivePosts = posts[0:5:1]
    return render_template('home.html',posts=fivePosts)

@app.route('/users')
def showAllUsers():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html',users=users)

@app.route('/users/new')
def showNewUserForm():
    return render_template('newUser.html')

@app.route('/users/new', methods=['POST'])
def addNewUser():
    firstName = request.form['first-name']
    lastName = request.form['last-name']
    imageUrl = request.form['image-url']

    if not firstName or not lastName:
        flash('First Name and Last Name cannot be blank','error')
        return redirect (request.referrer)

    newUser = User(first_name=firstName, last_name = lastName, image_URL=imageUrl or None)
    db.session.add(newUser)
    db.session.commit()

    flash('Sign-up successful!', 'success')
    return redirect('/users')

@app.route('/users/<int:user_id>')
def getUserInfo(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('userDetails.html',user=user)


@app.route('/users/<int:user_id>/edit')
def showEditUserForm(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('editUser.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def editUserInfo(user_id):
    
    user=User.query.get_or_404(user_id)
    
    firstName = request.form['first-name']
    lastName = request.form['last-name']
    imageUrl = request.form['image-url']

    user.first_name = firstName
    user.last_name = lastName
    user.image_URL = imageUrl

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def deleteUser(user_id):
    user = User.query.get(user_id)
    
    if user:
        Post.query.filter_by(user_id=user_id).delete(synchronize_session=False)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', 'success')
    else:
        flash('User not found', 'error')
    
    return redirect('/users')



@app.route('/users/<int:user_id>/posts/new')
def showPostForm(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('postForm.html',user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handleNewPostSubmission(user_id):
    title = request.form['title']
    content = request.form['content']

    if not content or not title:  # Check if content is empty
        flash('Title and content cannot be empty', 'error')
        return redirect(request.referrer)

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    flash('Post created!', 'success')
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def showPost(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',post=post)

@app.route('/posts/<int:post_id>/edit')
def showPostEditForm(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('postEdit.html',post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handleEditSubmission(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def deletePost(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect('/users')

    
@app.errorhandler(404)
def page_not_found(e):
    #render template for custom 404 message
    return render_template('404.html'), 404
