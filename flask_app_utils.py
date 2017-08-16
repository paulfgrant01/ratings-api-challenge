#!/usr/bin/python3
""" Flask Ratings utilities """

from requests import get

MOVIE_NAMES = {
    1: 'Batman Begins',
    2: 'The Dark Knight',
}
MOVIE_RATINGS = {
    1: 100,
    2: 98,
}
OMDB_RATINGS = {
    'Internet Movie Database': 'imdbRating',
    'Metacritic': 'metascore'
}
API_KEY = '8bdd5583'
OMDB_URL = 'http://www.omdbapi.com/?t={movie_name}&apikey={api_key}'

def update_movie_list(movie, rating):
    """ Update Movies """
    id_ = None
    if movie not in MOVIE_NAMES.values():
        id_ = max(MOVIE_NAMES.keys()) + 1
        MOVIE_NAMES[id_] = movie
    else:
        for movie_id, movie_name in MOVIE_NAMES.items():
            if movie_name == movie:
                id_ = movie_id
                break
    MOVIE_RATINGS[id_] = rating


def get_movie_detail(movie_id):
    """ Get Movie Detail """
    movie_name = MOVIE_NAMES[movie_id]
    movie_detail = {
        "id": int(movie_id),
        "title": movie_name,
        "rating": float(MOVIE_RATINGS[movie_id]),
    }
    third_party_ratings = get_third_party_ratings(movie_name)
    movie_detail.update(third_party_ratings)
    return movie_detail


def get_movie_list():
    """ Get Movies list """
    movie_list = []
    for movie_id in sorted(MOVIE_NAMES):
        movie_detail = get_movie_detail(movie_id)
        movie_list.append(movie_detail)
    return movie_list


def get_third_party_ratings(movie_name):
    """ Get ratings from 3rd party site """
    response = get(OMDB_URL.format(movie_name=movie_name, api_key=API_KEY))
    local_hash = {}
    json_data = response.json()
    if json_data.get('Ratings'):
        for rating_obj in json_data['Ratings']:
            if rating_obj['Source'] in OMDB_RATINGS:
                source = OMDB_RATINGS[rating_obj['Source']]
                value = rating_obj['Value'].split('/')[0]
                local_hash[source] = value
    return local_hash
