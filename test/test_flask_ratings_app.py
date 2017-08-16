#!/usr/bin/env python3
""" Test suite for Flass ratings app """

import unittest
import os
import json
import requests

HEADERS = {'content-type': 'application/json'}
MOVIES = ['Batman Begins', 'The Dark Knight']
NEW_MOVIE = {"Pauls Movie": "56"}
MOVIE_NAME = 'Pauls Movie'
UPDATED_MOVIE = {"Pauls Movie": "23"}
NOT_A_MOVIE = 'This really should not be here'
MOVIE_BY_ID = {
    'title': 'Batman Begins',
    'id': 1,
    'rating': 100.0,
    'metascore': '70',
    'imdbRating': '8.3'}
NOT_MOVIE_BY_ID = {'title': 'Pauls Movie', 'id': 3, 'rating': 23.0}


class FlaskAppTestSuite(unittest.TestCase):
    """ Test suite for Flass ratings app """

    def setUp(self):
        self.app_host = os.getenv('FLASK_APP_HOST', 'localhost')
        self.app_port = os.getenv('FLASK_APP_PORT', '10702')
        self.url = 'http://{}:{}/movies'.format(self.app_host, self.app_port)

    def test_get_movies_success(self):
        """ Test successful GET on /movies """
        response = requests.get(self.url)
        found = 0
        for result in response.json():
            for movie_name in MOVIES:
                if movie_name in result['title']:
                    found += 1
        self.assertTrue(found == 2)

    def test_get_movies_failure(self):
        """ Test failure GET on /movies """
        response = requests.get(self.url)
        found = None
        for result in response.json():
            found = False
            if NOT_A_MOVIE in result['title']:
                found = True
                break
        self.assertFalse(found)

    def test_post_movies_success(self):
        """ Test successful POST on /movies """
        response = requests.post(self.url, data=json.dumps(NEW_MOVIE), headers=HEADERS)
        found = None
        for result in response.json():
            if MOVIE_NAME in result['title']:
                found = True
                break
        self.assertTrue(found)

    def test_post_movies_failure(self):
        """ Test failure POST on /movies """
        response = requests.post(self.url, data=json.dumps(NEW_MOVIE), headers=HEADERS)
        found = False
        for result in response.json():
            if NOT_A_MOVIE in result['title']:
                found = True
                break
        self.assertFalse(found)

    def test_put_movies_success(self):
        """ Test successful PUT on /movies """
        response = requests.put(self.url, data=json.dumps(UPDATED_MOVIE), headers=HEADERS)
        rating = None
        for result in response.json():
            if MOVIE_NAME in result['title']:
                rating = result['rating']
                break
        self.assertTrue(rating == 23.0)

    def test_put_movies_failure(self):
        """ Test failure PUT on /movies """
        requests.put(self.url, data=json.dumps(NEW_MOVIE), headers=HEADERS)
        response = requests.put(self.url, data=json.dumps(UPDATED_MOVIE), headers=HEADERS)
        rating = None
        for result in response.json():
            if MOVIE_NAME in result['title']:
                rating = result['rating']
                break
        self.assertFalse(rating == 56.0)

    def test_get_movie_by_id_success(self):
        """ Test successful GET on /movie/<ID> """
        response = requests.get('{}/{}'.format(self.url, 1))
        self.assertTrue(response.json() == MOVIE_BY_ID)

    def test_get_movie_by_id_failure(self):
        """ Test failure GET on /movie/<ID> """
        response = requests.get('{}/{}'.format(self.url, 1))
        self.assertFalse(response.json() == NOT_MOVIE_BY_ID)


if __name__ == '__main__':
    unittest.main()
