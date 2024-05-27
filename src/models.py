import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    biography = Column(String(250))

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    photo_url = Column(String(250))
    caption = Column(Text)
    date = Column(DateTime)
    likes = relationship("Like", back_populates="post")
    comments = relationship("Comment", back_populates="post")

class Story(Base):
    __tablename__ = 'story'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(250))
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="stories")

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="likes")
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", back_populates="likes")
    comment_id = Column(Integer, ForeignKey('comment.id'))
    comment = relationship("Comment", back_populates="likes")
    story_id = Column(Integer, ForeignKey('story.id'))
    story = relationship("Story", back_populates="likes")


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="comments")
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    post = relationship("Post", back_populates="comments")

class DirectMessage(Base):
    __tablename__ = 'direct_message'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    date = Column(DateTime)
    sender_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    following_id = Column(Integer, ForeignKey('user.id'), nullable=False)


class Hashtag(Base):
    __tablename__ = 'hashtag'
    id = Column(Integer, primary_key=True)
    text = Column(String(50), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", back_populates="hashtags")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
