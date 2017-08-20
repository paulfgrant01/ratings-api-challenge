""" DAO for persistence """

from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from app.models.models import Movie

# Implemented DAOS
IMPLEMENTED_DAOS = ['SQLITE']

# Interface
class DAO(metaclass=ABCMeta):
    """ Interface that must be extended by DAO subclasses """

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

    @staticmethod
    def dao_factory(app):
        type_ = app.config['DAO_TYPE']
        # Check DAO_TYPE is in IMPLEMENTED_DAOS
        if type_ not in IMPLEMENTED_DAOS:
            # Raise custom exception if DAO_TYPE is not implemented
            raise DAONotImplemented('Available DAOs are {}'.format(IMPLEMENTED_DAOS))

        # Concat DAO_TYPE with DAO e.g. SQLITEDAO
        dao_object = type_ + 'DAO'

        # Get DAO object from imported objects
        dao = globals()[dao_object]

        # Return DAO object
        return dao(app)


class SQLITEDAO(DAO):
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
        self.engine = create_engine('sqlite:///' + self.db_loc)

    # Start session with db
    def start_session(self):
        """ Start db session """
        session_maker = sessionmaker(bind=self.engine)
        # Add session to object
        self.session = session_maker()

    # Used to decorate similar queries
    def decorate_query(query):
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

    # Will use decorate_query decorator
    @decorate_query
    def get_all_movies(self, **kwargs):
        """ Get all movies """
        # Get limit from kwargs
        limit = kwargs['limit']

        # Query all movies descending on movie id with enforced limit
        movies = self.session.query(Movie).order_by(desc(Movie.id)).limit(limit).all()

        # Convert to json and return
        return convert_to_json(movies, Movie)

    # Will use decorate_query decorator
    @decorate_query
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

    # Will use decorate_query decorator
    @decorate_query
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
        error = None

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
        # If movie exists return an error
        else:
            error = "Movie already exists"

        # Close session with db
        self.session.close()
        return error

    # Update Movie
    def update_movie(self, **kwargs):
        """ Update Movie """
        error = None

        # Start session with db
        self.start_session()

        # Query for Movie object
        query = self.session.query(Movie)

        # Get movie, filter by title
        movie = query.filter(Movie.title == kwargs['title']).first()
        # If movie exists update it
        if movie:
            # Updating Movie object rating
            movie.rating = kwargs['rating']

            # Commit update
            self.session.commit()

            # Close session with db
            self.session.close()
        # If movie does not exist set error
        else:
            error = 'Movie does not exist'

        # Close session with db
        self.session.close()
        return error

    # Delete movie
    def delete_movie(self, **kwargs):
        """ Delete Movie, used for testing, unimplemeneted for client use """
        # Start session with db
        self.start_session()
        # Query for movie object
        query = self.session.query(Movie)

        if 'id_' in kwargs:
            # Query for movie by id
            query = query.filter(Movie.id == kwargs['id_'])
        else:
            # Query for movie by title
            query = query.filter(Movie.title == kwargs['title'])
        # Find the object
        movie = query.one()

        # Delete oject from db
        self.session.delete(movie)

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
