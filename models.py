import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
import datetime
import os
import enum

Base = declarative_base()

class AssetTypes(enum.Enum):
    pass

class User(Base):
    """Contains user information"""
    __tablename__ = 'users'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    email = Column(String(150), nullable = False)

    boards = relationship("Boards")

    @property
    def serialize(self):
        return {
            'username': self.name,
            'id': self.id,
            'email': self.email,
            'boards': [board.serialize for board in self.boards]
        }

class Boards(Base):
    """Boards table"""
    __tablename__ = 'boards'
    __searchable__ = ['name', 'description']

    name = Column(String(80), nullable=False)
    description = Column(String(1000))
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    assets = relationship("Assets")

    @property
    def serialize(self):
        """Returns an object for JSONify purposes"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'user_id': self.user_id,
            'created': self.created_at,
            'updated': self.updated_at,
            'assets': [asset.serialize for asset in self.assets]
        }

class Assets(Base):
    """Asset table for images, etc. associated with a board"""
    __tablename__ = 'assets'
    __searchable__ = ['title', 'description']

    title = Column(String(200), nullable=False)
    id = Column(Integer, primary_key=True)
    #type = Column(Enum(AssetTypes))
    description = Column(String(5000))
    board_id = Column(Integer, ForeignKey(boards.id))
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    asset_url = Column(String(200))

    @property
    def serialize(self):
        """Returns an object for JSONify purposes"""
        return {
            'title': self.title,
            'id': self.id,
            #'type': self.type,
            'description': self.description,
            'board_id': self.board_id,
            'created': self.created_at,
            'updated': self.updated_at,
            'url': self.asset_url
        }


engine = create_engine('postgresql:///brandboards')
Base.metadata.create_all(engine)
