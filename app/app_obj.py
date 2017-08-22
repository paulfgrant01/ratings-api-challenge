""" This is where the main work of routing is carried out """

from flask import jsonify
from app.dao import DAO
from app.utils import Utils
from app.constants import USER_ACCESSING_MOVIE_LIST, USER_ACCESSED_MOVIE_LIST, \
    USER_ADDING_TO_MOVIE_LIST, USER_ADDED_TO_MOVIE_LIST, USER_UPDATING_MOVIE_IN_LIST, \
    USER_UPDATED_MOVIE_IN_LIST, USER_ACCESSING_MOVIE_BY_ID, USER_ACCESSED_MOVIE_BY_ID, \
    MOVIE_LIST_MIN, MOVIE_LIST_MAX, MOVIE_LIST_DEFAULT, MOVIE_ALREADY_EXISTS, \
    MOVIE_LIST_LIMIT_ERROR, MOVIE_LIST_RATING_ERROR, MOVIE_DOES_NOT_EXIST


class AppObject:
    """ This is where the main work of routing is carried out """

    def __init__(self, app):
        self.app = app
        self.dao = DAO.dao_factory(app)
        self.utils = Utils(self.app.config, self.app.logger)

    # Get movies
    def list_movies(self, request):
        """ Get movie list """
        # User is attempting to access movie list

        # Check user limit in request query falls within min/max limits
        limit = request.args.get("limit")
        if limit:
            if int(limit) < MOVIE_LIST_MIN or int(limit) > MOVIE_LIST_MAX:
                error = MOVIE_LIST_LIMIT_ERROR.format(MOVIE_LIST_MIN, MOVIE_LIST_MAX)
                return self.utils.convert_error(error), 400
        else:
            limit = MOVIE_LIST_DEFAULT

        # Log user accessing movie list
        self.app.logger.debug(USER_ACCESSING_MOVIE_LIST.format(request.remote_addr))

        # Get movie list via self.dao
        movie_list = self.dao.get_all_movies(limit=int(limit))
        # Access 3rd pary movie ratings
        for movie in movie_list:
            movie.update(self.utils.get_third_party_ratings(movie['title']))

        # Log user has successfully accessed movie list
        self.app.logger.debug(USER_ACCESSED_MOVIE_LIST.format(request.remote_addr))
        # Return jsonified movie list with success code
        return jsonify({'Movies': movie_list}), 200

    # Add movie to list
    def add_movie(self, request):
        """ Add movie to list """
        clientip = request.remote_addr
        data = request.json
        # Validate json against permitted schema
        validation_error = self.utils.validate_json(data)
        if validation_error:
            return jsonify(validation_error), 400

        # Access title/rating for ease of use
        title = data['title']
        rating = data['rating']

        # Ensure rating is between 1 and 5
        if float(rating) < 1 or float(rating) > 5:
            return self.utils.convert_error(MOVIE_LIST_RATING_ERROR), 400

        # Log user is attempting to add movie to list
        self.app.logger.debug(USER_ADDING_TO_MOVIE_LIST.format(clientip, title, rating))

        # Get user information
        user = self.dao.get_user(clientip=clientip)

        # Check if movie exists
        movie_exists = self.dao.get_movie_by_title(title=title)

        # If the movie is already there
        if movie_exists:

            # If the user has a rating for this movie (should be a PUT), return error
            if self.dao.get_user_rating(user_id=user['id'], movie_id=movie_exists['id']):
                return MOVIE_ALREADY_EXISTS, 400
            # If the user does not have rating add rating
            else:
                # Method will update movie rating and user rating
                update_movie_rating(rating, user['id'], movie_exists['id'])
        else:
            # Add movie with rating
            movie = self.dao.add_movie(title=title, rating=rating)

            # Add user rating to rating table
            self.dao.add_rating(
                rating=rating,
                user_id=user['id'],
                movie_id=movie['id'])

        # Log user successfully added movie to list
        message = USER_ADDED_TO_MOVIE_LIST.format(request.remote_addr, title, rating)
        self.app.logger.debug(message)
        self.app.logger.info(message)
        # Return success code
        return 'Make a new movie', 200

    # Update movie in list
    def update_movie(self, request):
        """ Update movie rating that is already in the list """
        clientip = request.remote_addr
        data = request.json
        # Validate json against permitted schema
        validation_error = self.utils.validate_json(data)
        if validation_error:
            return jsonify(validation_error), 400

        # Access title/rating for ease of use
        title = data['title']
        rating = data['rating']

        # Ensure rating is between 1 and 5
        if float(rating) < 1 or float(rating) > 5:
            return self.utils.convert_error(MOVIE_LIST_RATING_ERROR), 400

        # Log user is attempting to update movie in list
        self.app.logger.debug(USER_UPDATING_MOVIE_IN_LIST.format(clientip, title, rating))

        # Get user information
        user = self.dao.get_user(clientip=clientip)

        # Check if movie exists
        movie_exists = self.dao.get_movie_by_title(title=title)

        # If the movie does not exist (should be a POST), return error
        if not movie_exists:
            # Convert error to return to client
            return MOVIE_DOES_NOT_EXIST, 400

        # Method will update movie rating and user rating
        self.update_movie_rating(rating, user['id'], movie_exists['id'])

        # Log user has successfully updated movie in list
        message = USER_UPDATED_MOVIE_IN_LIST.format(clientip, title, rating)
        self.app.logger.debug(message)
        self.app.logger.info(message)
        return 'Updates the movie', 200

    # Get movie by id
    def get_movie_by_id(self, request, movie_id):
        """ Get Movie by Id """
        request_ip = request.remote_addr

        # Log is attempting to get movie by ID
        self.app.logger.debug(USER_ACCESSING_MOVIE_BY_ID.format(request_ip, movie_id))

        # Get movie by id via self.dao
        movie = self.dao.get_movie_by_id(id_=movie_id)
        if not movie:
            error = 'Movie does not exist with id {}!'.format(movie_id)
            return self.utils.convert_error(error), 400

        movie.update(self.utils.get_third_party_ratings(movie['title']))
        # Log user successfully accessed movie by ID
        message = USER_ACCESSED_MOVIE_BY_ID.format(request_ip, movie['title'], movie_id)
        self.app.logger.debug(message)
        self.app.logger.info(message)
        # Return jsonified movie list with success code
        return jsonify(movie), 200

    # Update the movie rating
    def update_movie_rating(self, rating, user_id, movie_id):
        """ Update the movie rating """
        # Add user rating to rating table
        self.dao.add_rating(rating=rating, user_id=user_id, movie_id=movie_id)

        # Get all ratings for this movie
        user_count, ratings_sum = self.dao.get_movie_ratings(movie_id=movie_id)

        # Calculate average rating
        average_rating = ratings_sum / user_count

        # Update movie rating
        self.dao.update_movie(id_=movie_id, rating=rating)
