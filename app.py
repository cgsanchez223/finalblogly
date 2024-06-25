"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.app_context().push() # I get an error if I do not put this

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True # Provides notes when running app.py in ipython
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False # Prevents warning message in ipython 
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """Home page. List of users."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

    # return redirect("/users")

@app.errorhandler(404)
def error_page(e):
    """404 Page Not Found"""

    return render_template('404.html'), 404

@app.route('/users')
def users():
    """Contains information on the users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def new_form():
    """Form to create a new user"""

    return render_template('users/new.html')

@app.route("/users/new", methods=["POST"])
def new_user():
    """Handles the form to create a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Page with info on specified user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Edits existing user page"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """"Form for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handles form to delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted")

    return redirect("/users")




# Post Routes
# Updated a few routes with tags

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show form to add a post for that user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'], content=request.form['content'], user=user, tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")



@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)



@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show form to edit a post, and to cancel"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)



@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle editing of a post. Redirect back to the post view."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tags_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tags_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"POST '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")



@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete the post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(F"/users/{post.user_id}")




# New Tag Routes
@app.route('/tags')
def tags_page():
    """Lists all tags, with links to the tag detail page."""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Shows a form to add a new tag."""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)



@app.route('/tags/new', methods=["POST"])
def new_tags():
    """Process add form, adds tag, and redirect to tag list."""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added")

    return redirect("/tags")



@app.route('/tags/<int:tag_id>')
def show_tags(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)



@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show edit form for a tag."""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)




@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tags(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited")

    return redirect("/tags")



@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tags(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted")

    return redirect("/tags")