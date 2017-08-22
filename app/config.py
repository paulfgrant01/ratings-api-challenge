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
    FLASK_APP_HOST = '127.0.0.1'
    #FLASK_APP_HOST = '54.209.200.143'

    # OMDB api access key
    API_KEY = '8bdd5583'

    # SQLDAO type
    DAO_TYPE = 'SQLADAO'
    # DB Name
    DB_NAME = 'ymdb.db'
    # SQLITE3 DB Location
    DB_LOC = 'sqlite:///{}/ymdb.db'.format(BASEDIR)
    # Implemented DAOS
    IMPLEMENTED_DAOS = ['SQLADAO']

