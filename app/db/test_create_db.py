""" Script to create db and insert initial data """

import sqlite3
import os
import sys

# Db name
DB = 'ymdb.db'

# Initial data to add
INITIAL_DATA = [
    {'title': 'Batman Begins', 'rating': '4.2'},
    {'title': 'The Dark Knight', 'rating': '3'},
]

def main():    
    """ Main """
    # If db exists exit
    if os.path.isfile(DB):
        print('DB already exists!')
        sys.exit(0)

    # Get sqlite connection
    conn = sqlite3.connect(DB)

    # Get cursor
    cursor = conn.cursor()

    # Create table "movies"
    cursor.execute('CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY, title TEXT, rating TEXT)')
    
    # Iterate over INITIAL_DATA
    for id_ in range(len(INITIAL_DATA)):
        # Assign movie name
        movie_name  = INITIAL_DATA[id_]['title']
        # Assign movie rating
        rating = INITIAL_DATA[id_]['rating']

        # Insert data into db
        cursor.execute("INSERT INTO movies VALUES({}, '{}', {})".format(id_ + 1, movie_name, rating))
    # Commit data
    conn.commit()

    # Close cursor
    cursor.close()
    
    # Close connection
    conn.close()


main()
