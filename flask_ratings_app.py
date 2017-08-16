#!/usr/bin/env python3
""" Flask Ratings application """

from os import environ
from flask import Flask, jsonify, request
from flask_app_utils import get_movie_list, get_movie_detail, update_movie_list, MOVIE_NAMES

APP = Flask(__name__)
PORT = int(environ['FLASK_APP_PORT'])

@APP.route('/movies', methods=['GET'])
def list_movies():
    """ Get movie list """
    movie_list = get_movie_list()
    return jsonify(movie_list)


@APP.route('/movies', methods=['POST'])
def add_movie():
    """ Add movie to list """
    movie, rating = request.json.popitem()
    update_movie_list(movie, rating)
    movie_list = get_movie_list()
    return jsonify(movie_list)


@APP.route('/movies', methods=['PUT'])
def update_movie():
    """ Update movie rating that is already in the list """
    movie, rating = request.json.popitem()
    update_movie_list(movie, rating)
    movie_list = get_movie_list()
    return jsonify(movie_list)


@APP.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    """ Get Movie by Id """
    movie_detail = {}
    if movie_id in MOVIE_NAMES.keys():
        movie_detail = get_movie_detail(movie_id)
    return jsonify(movie_detail)


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=PORT, debug=True, threaded=True)
