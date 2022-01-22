import os
from sqlalchemy.orm import (
    scoped_session, relationship,
    sessionmaker
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from dotenv import load_dotenv

load_dotenv()

basedir = os.getcwd()
engine = create_engine(os.getenv('connection_string'))
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base = declarative_base(bind=engine)
Base.query = session.query_property()


class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(Boolean, default=False) # True => completed, False => in progress
    due_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates="todo_list")


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), index=True, unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    todo_list = relationship('Todo', back_populates="user")