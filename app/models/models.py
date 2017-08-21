""" Movie model for ORM """
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator

# pylint: disable=abstract-method,too-few-public-methods,invalid-name

# All models must extend from this
BASE = declarative_base()

# Decorator to change rating output to float
class StringFloat(TypeDecorator):
    """ Decorator to change rating output to float """

    impl = String

    def process_literal_param(self, value, dialect):
        return str(float(value)) if value is not None else None

    process_bind_param = process_literal_param

    def process_result_value(self, value, dialect):
        return float(value) if value is not None else None


class Movie(BASE):
    """ Movie Object for ORM """
    # Database table name
    __tablename__ = 'movies'

    # Movie id in database, integer and set to primary key
    id = Column(Integer, primary_key=True)
    # Movie title in databse, 255 chars with index
    title = Column(String(255), index=True)
    # Movie rating in databse, decorator
    rating = Column(StringFloat)


class Users(BASE):
    """ Users Object for ORM """
    # Database table name
    __tablename__ = 'users'

    # User id in database, integer and set to primary key
    id = Column(Integer, primary_key=True)
    # User ip in databse, 255 chars with index
    clientip = Column(String(255), index=True)


class Ratings(BASE):
    """ Rating Object for ORM """
    # Database table name
    __tablename__ = 'ratings'

    # User id in database, integer and set to primary key
    user_id = Column(Integer, primary_key=True)
    # Movie id in database, integer
    movie_id = Column(Integer)
    # Movie rating in databse, decorator
    rating = Column(StringFloat)
