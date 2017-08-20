""" Flask Ratings utilities """

import sys
from requests import get
from jsonschema import validate, ValidationError, SchemaError
from app.constants import OMDB_RATINGS, OMDB_BASE_URL, POST_PUT_SCHEMA, JSON_ERROR_OBJECT
from flask import jsonify

class Utils:
    """ Flask Ratings utilities """

    def __init__(self, config, logger):
        # Get config file from application
        self.config = config
        # Get logger from application
        self.logger = logger

    def get_third_party_ratings(self, movie_name):
        """ Get ratings from 3rd party site """
        omdb_ratings = OMDB_RATINGS
        # Omdb url to get remote 3rd part ratings
        omdb_url = '{}/?t={}&apikey={}'.format(OMDB_BASE_URL, movie_name, self.config['API_KEY'])

        # local hash to store results before returning
        local_hash = {}
        # Send request to OMDB
        response = get(omdb_url)
        # Extract json response
        json_data = response.json()
        # check results object has 'Ratings' before proceeding
        if json_data.get('Ratings'):
            for rating_obj in json_data['Ratings']:
                # Iterate all ratings
                if rating_obj['Source'] in omdb_ratings:
                    # Get ratings name from respose via constant dict
                    source = omdb_ratings[rating_obj['Source']]
                    # extract value as we want it e.g 8 vs 8/10
                    value = rating_obj['Value'].split('/')[0]
                    # add value to local hash
                    local_hash[source] = value
        # Return local hash of ratings to update stored movies
        return local_hash

    def validate_json(self, received_json):
        """ Validate put/post json """
        error = None
        try:
            # Valide json matches our schema
            validate(received_json, POST_PUT_SCHEMA)
        # Catch jsonschema specific Exceptions
        except (ValidationError, SchemaError):
            # Split error object to return to client
            exc_obj = str(sys.exc_info()[1]).split('\n')[0]
            # Json shema error constant
            error = JSON_ERROR_OBJECT
            # Update detail in object
            error['errors'][0]['detail'] = exc_obj
        return error

    def convert_error(self, error):
        """ Convert error into JSON schema error """
        # Json shema error constant
        full_error = JSON_ERROR_OBJECT
        # Update detail in object
        full_error['errors'][0]['detail'] = error
        # Return jsonified object
        return jsonify(full_error)
