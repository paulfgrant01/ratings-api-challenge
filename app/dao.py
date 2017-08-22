""" DAO for persistence """

import os
from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, desc, func, update
from sqlalchemy.orm import sessionmaker
from app.models.models import Movie, Users, Ratings, BASE
from app.constants import INITIAL_DB_DATA

# Interface
class DAO(metaclass=ABCMeta):
    """ Interface that must be extended by DAO subclasses """

    @staticmethod
    def dao_factory(app):
        type_ = app.config['DAO_TYPE']
        # Check DAO_TYPE is in IMPLEMENTED_DAOS
        if type_ not in app.config['IMPLEMENTED_DAOS']:
            # Raise custom exception if DAO_TYPE is not implemented
            raise DAONotImplemented('Available DAOs are {}'.format(IMPLEMENTED_DAOS))

        # Get DAO object from imported objects
        dao = globals()[app.config['DAO_TYPE']]

        # Return DAO object
        return dao(app)

    # Required to get all movies
    @abstractmethod
    def get_all_movies(self, **kwargs): pass

    # Required to get movie by id
    @abstractmethod
    def get_movie_by_id(self, **kwargs): pass

    # Required to add movie
    @abstractmethod
    def add_movie(self, **kwargs): pass

    # Required to update movie
    @abstractmethod
    def update_movie(self, **kwargs): pass

    # Required to get user 
    @abstractmethod
    def get_user(self, **kwargs): pass

    # Required to get a movie's ratings
    @abstractmethod
    def get_movie_ratings(self, **kwargs): pass

    # Required to get a user's rating of a movie
    @abstractmethod
    def get_user_rating(self, **kwargs): pass


class SQLADAO(DAO):
    """ DAO for sqlite """

    def __init__(self, app):
        # Add db location to object
        self.db_loc = app.config['DB_LOC']
        # Define attribute
        self.session = None
        # Object connection
        self.connect()

    # Connect to database
    def connect(self):
        """ DB connection """
        # Will connect to database
        self.engine = create_engine(self.db_loc)
        # If db does not exist create it
        if not os.path.exists(self.db_loc):
            # Create all tables
            BASE.metadata.create_all(self.engine)
            # Insert all items in db
            for item in INITIAL_DB_DATA:
                self.add_movie(title=item['title'], rating=item['rating'])
                
    # Start session with db
    def start_session(self):
        """ Start db session """
        session_maker = sessionmaker(bind=self.engine)
        # Add session to object
        self.session = session_maker()

    # Used to decorate similar queries
    def select_query(query):
        """ Decorator for similar queries """
        def wrap(self, **kwargs):
            """ Wrap function """
            # Start session for wrapped function
            self.start_session()

            # Execute function and get return object
            return_obj = query(self, **kwargs)

            # Close session
            self.session.close()
            return return_obj
        return wrap

    # Will use select_query decorator
    @select_query
    def get_all_movies(self, **kwargs):
        """ Get all movies """
        # Get limit from kwargs
        limit = kwargs['limit']

        # Query all movies descending on movie id with enforced limit
        movies = self.session.query(Movie).order_by(desc(Movie.id)).limit(limit).all()

        # Convert to json and return
        return convert_to_json(movies, Movie)

    # Will use select_query decorator
    @select_query
    def get_movie_by_id(self, **kwargs):
        """ Get movie by id """
        # Initialize return_obj
        return_obj = None

        # Query for movie, filtered by id
        movie = self.session.query(Movie).filter_by(id=kwargs['id_']).first()
        if movie:
            # If movie exists convert to json before returning
            return_obj = convert_to_json([movie], Movie)[0]
        return return_obj

    # Will use select_query decorator
    @select_query
    def get_movie_by_title(self, **kwargs):
        """ Get movie by title """
        return_obj = None
        # Query for movie, filtered by title
        movie = self.session.query(Movie).filter(Movie.title.like(kwargs['title'])).first()
        if movie:
            # If movie exists convert to json before returning
            return_obj = convert_to_json([movie], Movie)[0]
        return return_obj

    # Add a movie to db
    def add_movie(self, **kwargs):
        """ Add movie """
        # Start session with db
        self.start_session()

        # Query for movie, filtered by title
        movie = self.session.query(Movie).filter(Movie.title.like(kwargs['title'])).first()

        # if movie does not exist add it
        if not movie:
            # Update Movie object
            movie = Movie(title=kwargs['title'], rating=kwargs['rating'])

            # Add updated object to session
            self.session.add(movie)

            # Commit update to db
            self.session.commit()

        return_obj = convert_to_json([movie], Movie)[0]
        # Close session with db
        self.session.close()
        return return_obj

    # Update Movie
    def update_movie(self, **kwargs):
        """ Update Movie """
        # Start session with db
        self.start_session()
        # Query for Movie object
        movie = self.session.query(Movie).filter(Movie.id == kwargs['id_']).first()
        # Update the object
        movie.rating = kwargs['rating']
        # Commit update
        self.session.commit()
        # Close session with db
        self.session.close()
        #return error

    def get_user(self, **kwargs):
        """ Add user """
        # Start session with db
        self.start_session()

        # Query for user, filtered by clientip
        user = self.session.query(Users).filter_by(clientip=kwargs['clientip']).first()

        # if user does not exist add them
        if not user:
            # Update User object
            user = Users(clientip=kwargs['clientip'])

            # Add updated object to session
            self.session.add(user)

            # Commit update to db
            self.session.commit()

        return_obj = convert_to_json([user], Users)[0]

        # Close session with db
        self.session.close()
        return return_obj

    def add_rating(self, **kwargs):
        """ Add Rating """
        # Start session with db
        self.start_session()

        # Query to get the Ratings table
        query = self.session.query(Ratings)

        # Update Rating object
        rating = Ratings(
            rating=kwargs['rating'],
            user_id=kwargs['user_id'],
            movie_id=kwargs['movie_id'])

        # Add updated object to session
        self.session.add(rating)

        # Commit updated object to db
        self.session.commit()

        # Close session with db
        self.session.close()
        return rating

    # Will use select_query decorator
    @select_query
    def get_movie_ratings(self, **kwargs):
        """ Get a movie's ratings """
        # Query ratings object
        ratings = self.session.query(Ratings)
        # Get count of users who have provided a movie rating
        user_count = ratings.filter_by(movie_id=kwargs['movie_id']).count()
        # Get count of all users who have provided a movie rating
        ratings_sum = self.session.query(func.sum(Ratings.rating)).scalar()

        return user_count, ratings_sum

    # Will use select_query decorator
    @select_query
    def get_user_rating(self, **kwargs):
        """ Get a user's rating of a movie """
        # Query ratings object
        ratings = self.session.query(Ratings.rating)
        rating = ratings.filter_by(
            user_id=kwargs['user_id'],
            movie_id=kwargs['movie_id']).scalar()
        return rating

    # Delete User
    def delete_user(self, **kwargs):
        """ Delete User and their ratings, used for testing, unimplemeneted for client use """
        # Start session with db
        self.start_session()
        # Query for and delete user ratings
        self.session.query(Ratings).filter_by(user_id=kwargs['user_id']).delete()
        # Query for and delete user
        self.session.query(Users).filter_by(id=kwargs['user_id']).delete()
        # Commit 
        self.session.commit()
        # Close session with db
        self.session.close()

    # Delete movie
    def delete_movie(self, **kwargs):
        """ Delete Movie, used for testing, unimplemeneted for client use """
        # Start session with db
        self.start_session()

        if 'id_' in kwargs:
            # Query for movie by id
            self.session.query(Movie).filter_by(id=kwargs['id_']).delete()
        else:
            # Query for movie by title
            self.session.query(Movie).filter_by(title=kwargs['title']).delete()

        # Commit delete
        self.session.commit()

        # Close session with db
        self.session.close()



# Convert result set to json format
def convert_to_json(result_set, table):
    """ Convert result set to json objects """
    # pylint: disable=protected-access
    json_list = []
    # For each result
    for result in result_set:
        # local hash to be added to json list
        local_hash = {}

        # Iterate over Movie model column names
        for column in table.__table__.columns._data.keys():
            # Add result from object to hash
            local_hash[column] = getattr(result, column)

        # Add to json list to be returned to client
        json_list.append(local_hash)
    return json_list


# Custom exception extends ValueError
class DAONotImplemented(ValueError):
    """ Custom exception extends ValueError """
    def __init__(self, message):
        self.message = message
        # Calling ValueError init method
        super().__init__()
