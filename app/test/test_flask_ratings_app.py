""" Test suite for Flask ratings app """

import unittest
import json
import requests
from flask import Flask
from app.config import Config
from app.constants import MOVIE_LIST_MIN, MOVIE_LIST_MAX, OMDB_RATINGS, MOVIE_ALREADY_EXISTS, \
    MOVIE_DOES_NOT_EXIST
from app.dao import SQLADAO

CLIENT_IP = '127.0.0.1'
# Headers to be sent with post/put
HEADERS = {'content-type': 'application/json'}
# Movies required for testing
MOVIES_TO_ADD = [
    {"title": "This is test 1", "rating": 4.0},
    {"title": "This is test 2", "rating": 7.0},
    {"title": "This is test 3", "rating": 7.0},
    {"title": "This is test 4", "rating": 7.0},
    {"title": "This is test 5", "rating": 7.0},
    {"title": "This is test 6", "rating": 7.0},
    {"title": "This is test 7", "rating": 7.0},
    {"title": "This is test 8", "rating": 7.0},
    {"title": "This is test 9", "rating": 7.0},
    {"title": "This is test 10", "rating": 7.0},
    {"title": "This is test 11", "rating": 7.0},
]
# Incorrect rating used to update a movie via put
UPDATE_MOVIE_INVALID_RATING = {"title": "This is test 1", "rating": 7}
# Data used to update a movie via put
UPDATE_MOVIE = {"title": "This is test 1", "rating": 3}
# Used to cause invalid schema response
INVALID_SCHEMA_MOVIE = {"Pauls Movie": "23"}
# Minimum limit for requesting movies
LIMIT_MIN = '?limit={}'.format(MOVIE_LIST_MIN)
# Maximum limit for requesting movies
LIMIT_MAX = '?limit={}'.format(MOVIE_LIST_MAX)
# Wrong maximum limit for requesting movies
LIMIT_MAX_WRONG = '?limit={}'.format(MOVIE_LIST_MAX + 1)
# Wrong minimum limit for requesting movies
LIMIT_MIN_WRONG = '?limit={}'.format(MOVIE_LIST_MIN - 1)
# Test OMDB ratings
OMDB_MOVIE = \
    {'id': 1, 'metascore': '70', 'imdbRating': '8.3', 'title': 'Batman Begins', 'rating': '86.0'}


class FlaskAppTestSuite(unittest.TestCase):
    """ Test suite for Flass ratings app """

    # Setup before test case execution
    def setUp(self):
        """ Set up before executing test cases """
        # Get flask app
        app = Flask(__name__)
        # Get flask app configuration
        app.config.from_object(Config)
        # Add app to object for later use
        self.app = app
        # Setup base request url
        self.url = 'http://{}:{}/movies'.format(
            self.app.config['FLASK_APP_HOST'],
            self.app.config['FLASK_APP_PORT'])
        # Get data access object
        self.db_dao = SQLADAO(self.app)

    # Tear down after test case execution
    def tearDown(self):
        """ Tear down after test case execution """
        # Delete User and their ratings
        delete_user_and_ratings(self.db_dao)
       

    def test_get_movies(self):
        """ Test successful GET on /movies """
        # Add required movies first
        add_movies(MOVIES_TO_ADD, self.db_dao)
        # Get movies from remote
        response = requests.get(self.url + LIMIT_MAX)
        found = 0
        # Check if the movies added above are being returned
        for result in response.json()['Movies']:
            for movie in MOVIES_TO_ADD:
                if movie['title'] in result['title']:
                    found += 1
                    break
        # Delete movies that were created at the start
        delete_movies(MOVIES_TO_ADD, self.db_dao)
        # Carry out assertion
        self.assertTrue(found == len(MOVIES_TO_ADD))

    def test_get_limit_11(self):
        """ Test successful GET on /movies with limit 11"""
        # Add required movies first
        add_movies(MOVIES_TO_ADD, self.db_dao)
        # Get movies from remote
        response = requests.get(self.url + LIMIT_MIN)
        # Get reponse objects movies to variable
        found_movies = response.json()['Movies']
        # Delete movies that were created at the start
        delete_movies(MOVIES_TO_ADD, self.db_dao)
        # Carry out assertion
        self.assertTrue(len(found_movies) == len(MOVIES_TO_ADD))

    def test_get_limit_max_wrong(self):
        """ Test unsuccessful GET on /movies with limit MAX wrong"""
        # Add required movies first
        add_movies(MOVIES_TO_ADD, self.db_dao)
        # Get movies from remote
        response_obj = requests.get(self.url + LIMIT_MAX_WRONG)
        # Get reponse object data to variable
        response = response_obj.json()
        # Delete movies that were created at the start
        delete_movies(MOVIES_TO_ADD, self.db_dao)
        # Error that should be returned
        error = "Number of movies to return must be between 11 and 10000!"
        # Carry out assertion
        self.assertTrue(response['errors'][0]['detail'] == error)

    def test_get_limit_min_wrong(self):
        """ Test unsuccessful GET on /movies with limit MIN wrong"""
        # Add required movies first
        add_movies(MOVIES_TO_ADD, self.db_dao)
        # Get movies from remote
        response_obj = requests.get(self.url + LIMIT_MIN_WRONG)
        # Get reponse object data to variable
        response = response_obj.json()
        # Delete movies that were created at the start
        delete_movies(MOVIES_TO_ADD, self.db_dao)
        # Error that should be returned
        error = "Number of movies to return must be between 11 and 10000!"
        # Carry out assertion
        self.assertTrue(response['errors'][0]['detail'] == error)

    def test_post_movies_success(self):
        """ Test successful POST on /movies """
        # Add movie
        response = requests.post(self.url, data=json.dumps(MOVIES_TO_ADD[0]), headers=HEADERS)
        # Delete created movie
        delete_movies([MOVIES_TO_ADD[0]], self.db_dao)
        # Carry out assertion
        self.assertTrue(response.status_code == 200)

    def test_post_movies_fail_already_exists(self):
        """ Test unsuccessful POST on /movies, movie exists """
        # Add required movie first
        response_obj = requests.post(self.url, data=json.dumps(MOVIES_TO_ADD[0]), headers=HEADERS)
        # Double post to cause failure
        response_obj = requests.post(self.url, data=json.dumps(MOVIES_TO_ADD[0]), headers=HEADERS)
        # Delete movies that were created at the start
        delete_movies([MOVIES_TO_ADD[0]], self.db_dao)
        # Carry out assertion
        status_code = response_obj.status_code
        error = response_obj.text
        self.assertTrue(error == MOVIE_ALREADY_EXISTS and status_code == 400)

    def test_post_movies_fail_invalid_schema(self):
        """ Test unsuccessful POST on /movies, invalid schema """
        # Post invalid schema
        response_obj = requests.post(
            self.url, data=json.dumps(INVALID_SCHEMA_MOVIE),
            headers=HEADERS)
        # Carry out assertion
        self.assertTrue(response_obj.status_code == 400)

    def test_post_movies_fail_invalid_rating(self):
        """ Test unsuccessful PUT on /movies, invalid rating """
        # Post invalid rating
        response_obj = requests.post(
            self.url,
            data=json.dumps(UPDATE_MOVIE_INVALID_RATING), headers=HEADERS)
        # Carry out assertion
        self.assertTrue(response_obj.status_code == 400)

    def test_put_movie_success(self):
        """ Test successful PUT on /movies """
        # Add required movie first
        add_movies([MOVIES_TO_ADD[0]], self.db_dao)
        # Update movie on remote
        response_obj = requests.put(self.url, data=json.dumps(UPDATE_MOVIE), headers=HEADERS)
        # Delete movie that was created at the start
        delete_movies([MOVIES_TO_ADD[0]], self.db_dao)
        # Carry out assertion
        self.assertTrue(response_obj.status_code == 200)

    def test_put_movie_does_not_exist(self):
        """ Test unsuccessful PUT on /movies, movie does not exist """
        # Attempt to update movie on remote
        response_obj = requests.put(self.url, data=json.dumps(UPDATE_MOVIE), headers=HEADERS)
        error = response_obj.text
        status_code = response_obj.status_code
        # Carry out assertion
        self.assertTrue(error == MOVIE_DOES_NOT_EXIST and status_code == 400)

    def test_put_movies_fail_invalid_schema(self):
        """ Test unsuccessful PUT on /movies, invalid schema """
        # Post invalid schema
        response_obj = requests.put(
            self.url,
            data=json.dumps(INVALID_SCHEMA_MOVIE), headers=HEADERS)
        # Carry out assertion
        self.assertTrue(response_obj.status_code == 400)

    def test_put_movies_fail_invalid_rating(self):
        """ Test unsuccessful PUT on /movies, invalid rating """
        # Post invalid rating
        response_obj = requests.put(
            self.url,
            data=json.dumps(UPDATE_MOVIE_INVALID_RATING), headers=HEADERS)
        # Carry out assertion
        self.assertTrue(response_obj.status_code == 400)

    def test_get_movie_by_id(self):
        """ Test successful get movie by id """
        # Add required movie first
        add_movies([MOVIES_TO_ADD[0]], self.db_dao)
        # Query for movie
        movie = self.db_dao.get_movie_by_title(title=MOVIES_TO_ADD[0]['title'])
        # Query for movie by id
        response_obj = requests.get(self.url + '/{}'.format(movie['id']))
        # Get reponse object data to variable
        response = response_obj.json()
        # Delete movie above
        delete_movies([MOVIES_TO_ADD[0]], self.db_dao)
        # Carry out assertion
        self.assertTrue(response['id'] == movie['id'])

    def test_get_movie_by_id_unsuccessful(self):
        """ Test unsuccessful get movie by id, movie does not exist """
        # Add required movie first
        add_movies([MOVIES_TO_ADD[0]], self.db_dao)
        # Query for movie
        movie = self.db_dao.get_movie_by_title(title=MOVIES_TO_ADD[0]['title'])
        # Delete movie above
        delete_movies([MOVIES_TO_ADD[0]], self.db_dao)
        # Query for movie by id
        response_obj = requests.get(self.url + '/{}'.format(movie['id']))
        # Get reponse object data to variable
        response = response_obj.json()
        # Error that should be returned
        error = 'Movie does not exist with id {}!'.format(movie['id'])
        # Carry out assertion
        self.assertTrue(response['errors'][0]['detail'] == error)

    def test_get_movie_by_id_omdb(self):
        """ Test get movie by id, with omdb ratings """
        # Get movie with ratings
        movie = self.db_dao.get_movie_by_title(title=OMDB_MOVIE['title'])
        # Get the same movie by id
        response_obj = requests.get(self.url + '/{}'.format(movie['id']))
        # Get reponse object data to variable
        response = response_obj.json()
        # e.g. imdbRating/metascore
        required_ratings = OMDB_RATINGS.values()
        # e.g. id/metascore/imdbRating/title/rating
        remote_ratings = response.keys()
        # Carry out assertion
        self.assertTrue(set(required_ratings).issubset(set(remote_ratings)))

def delete_user_and_ratings(dao):
    """ Delete user and their ratings """
    # Get user first
    user = dao.get_user(clientip=CLIENT_IP)
    if user:
        dao.delete_user(user_id=user['id'])

def add_movies(movies, dao):
    """ Add movies for testing """
    # Take a list of movies and add them via dao
    for movie in movies:
        dao.add_movie(title=movie['title'], rating=movie['rating'])

def delete_movies(movies, dao):
    """ Delete movies for testing """
    # Take a list of movies and delete them via dao
    for movie in movies:
        dao.delete_movie(title=movie['title'])
