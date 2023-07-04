"""Blogly application."""
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post, Tag
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
    tags = Tag.query.order_by(Tag.name)
    return render_template('postForm.html',user=user, tags=tags)

# @app.route('/users/<int:user_id>/posts/new', methods=['POST'])
# def handleNewPostSubmission(user_id):
#     title = request.form['title']
#     content = request.form['content']
#     tags = request.form.getlist('tags')

#     if not content or not title:  # Check if content is empty
#         flash('Title and content cannot be empty', 'error')
#         return redirect(request.referrer)

#     tagList = []

#     for tag in tags:
#         tag_obj = Tag.query.filter(Tag.name == tag).first()
#         if tag_obj:
#             tagList.append(tag_obj)

#     post = Post(title=title, content=content, user_id=user_id)

#     post.tags.extend(tagList)

#     db.session.add(post)
#     db.session.commit()

#     flash('Post created!', 'success')
#     return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
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
    tags = Tag.query.all()

    return render_template('postEdit.html',post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handleEditSubmission(post_id):
    title = request.form['title']
    content = request.form['content']
    tagIds = [int(num) for num in request.form.getlist('tags')]

    if not content or not title:  # Check if content is empty
        flash('Title and content cannot be empty', 'error')
        return redirect(request.referrer)

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    tags = Tag.query.filter(Tag.id.in_(tagIds)).all()

    post.tags=tags
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


@app.route('/tags')
def showTagList():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tagId>')
def tagDetails(tagId):
    tag = Tag.query.get_or_404(tagId)
    return render_template('tagDetail.html',tag=tag)

@app.route('/tags/new')
def newTagForm():
    return render_template('tagForm.html')

@app.route('/tags/new', methods=['POST'])
def handleNewTag():
    name = request.form['tag-name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tagId>/edit')
def showTagEditForm(tagId):
    tag = Tag.query.get_or_404(tagId)
    posts = Post.query.all()
    return render_template('tagEditForm.html',tag = tag, posts=posts)

@app.route('/tags/<int:tagId>/edit', methods=['POST'])
def handleTagEdit(tagId):
    name = request.form['tag-name']

    if not name:
        flash('Tag name required', 'error')
        return redirect(request.referrer)

    tag = Tag.query.get_or_404(tagId)
    posts = request.form.getlist('posts')
    postList = []
    for post in posts:
        p = Post.query.filter(Post.title == post).first()
        postList.append(p)
    tag.name = name
    tag.posts = postList
    # raise
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tagId>/delete', methods=['POST'])
def deleteTag(tagId):
    Tag.query.filter_by(id=tagId).delete()
    db.session.commit()
    return redirect('/tags')


