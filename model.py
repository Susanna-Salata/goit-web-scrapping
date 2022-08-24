from datetime import datetime

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_url = Column(String(250), nullable=False)
    rating = Column(Integer, nullable=False)
    title = Column(String(150), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    description = Column(String(2048), nullable=False)
    created = Column(DateTime, default=datetime.now())


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(2048), nullable=False)
    author = Column(String(150), nullable=True)
    author_details = Column(String(150), nullable=True)
    tag = Column(String(150), nullable=True)
    created = Column(DateTime, default=datetime.now())
