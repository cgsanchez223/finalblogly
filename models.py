"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"
#Image taken from solution.

class User(db.Model):
    """user profile"""

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
    @property
    def full_name(self):
        """Returns users full name"""

        return f"{self.first_name} {self.last_name}"
    


class Post(db.Model):
    """For blog posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                   primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, 
                           nullable=False, 
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Reformatted date"""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    

class PostTag(db.Model):
    """Tags that are on posts"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
    

class Tag(db.Model):
    """Can be added to posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)
    
    posts = db.relationship('Post', secondary="posts_tags", backref = "tags")
 




def connect_db(app):
    db.app = app
    db.init_app(app)