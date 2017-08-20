""" Flask application config file """

import os
import logging

class Config: # pylint: disable=too-few-public-methods
    """ Flask application config file """

    # LOG
    LOG = 'error.log'
    # Log level
    LOG_LEVEL = logging.DEBUG
    # Log format
    LOG_FORMAT = '%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d | %(funcName)s ' \
        '| %(message)s'

    # Application base directory
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Application server port
    FLASK_APP_PORT = 10702
    # Application server host
    FLASK_APP_HOST = 'localhost'

    # OMDB api access key
    API_KEY = '8bdd5583'

    # SQLITE3 DB
    DAO_TYPE = 'SQLITE'
    # SQLITE3 DB Location
    DB_LOC = BASEDIR + '/db/ymdb.db'
