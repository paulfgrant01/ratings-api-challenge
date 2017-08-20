""" Flask Ratings application """

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from app.app_obj import AppObject
from app.config import Config

# Initialize flask application
app = Flask(__name__)
# Load application configuration file
app.config.from_object(Config)
# Load app object to do the work
app_obj = AppObject(app)

# Route to access movie list
@app.route('/movies', methods=['GET'])
def list_movies():
    """ Get movie list """
    return app_obj.list_movies(request)


# Route to add movie to list
@app.route('/movies', methods=['POST'])
def add_movie():
    """ Add movie to list """
    return app_obj.add_movie(request)


# Route to update movie in list
@app.route('/movies', methods=['PUT'])
def update_movie():
    """ Update movie rating that is already in the list """
    return app_obj.update_movie(request)


# Route to get movie by id
@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    """ Get Movie by Id """
    return app_obj.get_movie_by_id(request, movie_id)


if __name__ == '__main__':
    # Rotating file handler to output to files up to 1MB before rollover
    handler = RotatingFileHandler(app.config['LOG'], maxBytes=10000, backupCount=1)
    # Initialize formatter
    formatter = logging.Formatter(app.config['LOG_FORMAT'])
    # Set handler formatter
    handler.setFormatter(formatter)
    # Setting log level based on config file
    handler.setLevel(app.config['LOG_LEVEL'])
    # Add handler to app logger
    app.logger.addHandler(handler)

    # Get app port from config
    port = app.config['FLASK_APP_PORT']
    # Run app with '0.0.0.0' to allow external access
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
