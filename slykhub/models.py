#SQLALchemy
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask import g, session , current_app
from . import db
# from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text


# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     created_on = Column(DateTime(), default=datetime.now)
#     updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
#     username = Column(String(100), nullable=False, unique=True) 
#     password = Column(Text, nullable=False)
#     slyks = relationship('Slyk', backref='owner')
    
# class Slyk(Base):
#     __tablename__ = 'slyk'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     created_on = Column(DateTime(), default=datetime.now)
#     updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
#     user_id = Column(Integer(), ForeignKey('user.id'))
#     name = Column(String(100), nullable=False)
#     api_key = Column(String(255), nullable=False, unique=True)

# # Base.metadata.create_all(engine)
class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        created_on = db.Column(db.DateTime(), default=datetime.now)
        updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
        username = db.Column(db.String(100), nullable=False, unique=True) 
        password = db.Column(db.Text, nullable=False)
        slyks = relationship('Slyk', backref='owner', lazy=True)
        active_slyk_id = db.Column(db.Integer())
    
class Slyk(db.Model):
    __tablename__ = 'slyk'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(255), nullable=False, unique=True)
