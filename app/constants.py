""" All constants and messages definitions go here """

""" OMDB Constants """
# OMDB Ratings is {OMDB Name: Our return name} 
OMDB_RATINGS = {
    'Internet Movie Database': 'imdbRating',
    'Metacritic': 'metascore'
}
# Base URL to send get requests for third party ratings
OMDB_BASE_URL = 'http://www.omdbapi.com'

""" Logger Constants """
# Log user attempting to access movie list with ip
USER_ACCESSING_MOVIE_LIST = '{}: Attempting to access movie list'
# Log user accessed movie list with ip
USER_ACCESSED_MOVIE_LIST = '{}: User accessed movie list'
# Log user attempting to add movie to list with ip, movie name, and rating
USER_ADDING_TO_MOVIE_LIST = '{}: User adding movie "{}" with rating {} to movie list'
# Log user adding movie to list with ip, movie name, and rating
USER_ADDED_TO_MOVIE_LIST = '{}: User added movie "{}" with rating {} to movie list'
# Log user attempting to update movie in list with ip, movie name, and rating
USER_UPDATING_MOVIE_IN_LIST = '{}: User updating movie "{}" with rating {} in movie list'
# Log user updated movie in list with ip, movie name, and rating
USER_UPDATED_MOVIE_IN_LIST = '{}: User updated movie "{}" with rating {} in movie list'
# Log user attempting to access movie in list by id with ip and movie id
USER_ACCESSING_MOVIE_BY_ID = '{}: User attempting to access movie by id {}'
# Log user accessed movie in list by id with ip and movie id
USER_ACCESSED_MOVIE_BY_ID = '{}: User accessed movie "{}" by id {}'
# Log Application Error
APPLICATION_ERROR = '{}: Something went wrong!'
# Schema to validate post/put json
POST_PUT_SCHEMA = {
    "type" : "object",
        "properties" : {
            "title" : {"type" : "string"},
            "rating" : {"type" : "number"},
        },
        "required": ["title", "rating"],
        "additionalProperties": False
}
# Error json to return to client
JSON_ERROR_OBJECT = {
    "errors": [{
        "status": "400",
        "detail": "{}"
    }]
}
# Get all movies list minimum limit
MOVIE_LIST_MIN = 11
# Get all movies list maximum limit
MOVIE_LIST_MAX = 10000
# Get all movies list default limit
MOVIE_LIST_DEFAULT = 11
# Movie limit request error 
MOVIE_LIST_LIMIT_ERROR = 'Number of movies to return must be between {} and {}!'
# Movie limit request error 
MOVIE_LIST_RATING_ERROR = 'Rating must be between 1 and 5!'
# Movie already exists error
MOVIE_ALREADY_EXISTS = 'Movie already exists, update via PUT!'
# Movie does not exist exists error
MOVIE_DOES_NOT_EXIST = 'Movie does not exist, add via POST!'
# Initial data to add to db
INITIAL_DB_DATA = [
    {'title': 'Batman Begins', 'rating': '4.2'},
    {'title': 'The Dark Knight', 'rating': '3'},
]
