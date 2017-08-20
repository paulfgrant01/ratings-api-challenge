# Ratings Aggregator API
***
### Synopsis
---
This project is a basic movie ratings application. Rest endpoints have been created to get/add/update movie ratings.

### Installation
---
In order to run this application you will need the following installed:

python3 and libraries:


> requests
> json
> flask
> sqlalchemy
> jsonschema


### Steps to install:                
```sh
$ git clone https://github.com/paulfgrant01/ratings-api-challenge.git
$ export PYTHONPATH=$PYTHONPATH:YOUR_DIRECTORY/ratings-api-challenge
$ cd ratings-api-challenge
$ export APPLICATION_DIRECTORY=`pwd`
$ cd app/db
$ python3 test_create_db.py
$ cd ../app
$ python3 run.py
```
### AWS Setup
To run agains AWS hosted app update your config file: 
```sh
$APPLICATION_DIRECTORY/ratings-api-challenge/app/configy.py:
```
And set the following values:
- FLASK_APP_PORT=10702
- FLASK_APP_HOST=54.209.200.143


# RESTful API Reference
Below are the API's provided by this application:
1. List all movies registered in the system (HTTP GET /movies)
2. Register a new movie (HTTP POST /movies), with a Title and Rating (combined user rating)
3. Update an existing movie registered in the system (HTTP PUT /movies)
4. Get details for a single movie registered in the system (HTTP GET /movies/123)

# Testing
---
Test suites are located in ratings-api-challenge/app/test and can be executed via:
```sh
$ cd $APPLICATION_HOME/app/test
$ nodetests
```
[This Jenkins CI server is scheduled to run every 15 minutes.](http://54.209.200.143:8080/jenkins/)

Ensure you have your PYTHONPATH is set to $APPLICATION_HOME
Set your HOST/PORT in $APPLICATION_HOME/app/config.py
- HOST = FLASK_APP_HOST = localhost|54.209.200.143 (AWS)
- PORT = FLASK_APP_PORT = 10702

To run from interpreter see below:

```python
>>> import requests
>>> import json
>>> HEADERS = {'content-type': 'application/json'}
### GET

>>> result = requests.get('http://HOST:PORT/movies')
>>> result.json()
{'Movies': [{'imdbRating': '9.0', 'metascore': '82', 'rating': 3.0, 'id': 2, 'title': 'The Dark Knight'}, {'imdbRating': '8.3', 'metascore': '70', 'rating': 4.2, 'id': 1, 'title': 'Batman Begins'}]}
>>> result.status_code
200

### POST

>>> import json
>>> data = {"title": "Donnie Darko", "rating": 4.6}
>>> request = requests.post('http://HOST:PORT/movies', data=json.dumps(data), headers=HEADERS)
>>> request.status_code
200
>>> request.text
'Make a new movie'
>>> request = requests.get('http://HOST:PORT/movies?limit=1000')
>>> request.json()
{'Movies': [{'imdbRating': '8.1', 'metascore': '88', 'rating': 4.6, 'id': 3, 'title': 'Donnie Darko'}, {'imdbRating': '9.0', 'metascore': '82', 'rating': 3.0, 'id': 2, 'title': 'The Dark Knight'}, {'imdbRating': '8.3', 'metascore': '70', 'rating': 4.2, 'id': 1, 'title': 'Batman Begins'}]}

### PUT

>>> data = {"title": "Donnie Darko", "rating": 4.6}
>>> request = requests.put('http://HOST:PORT/movies', data=json.dumps(data), headers=HEADERS)
>>> request.status_code
200
>>> request.text
'Updates the movie'
>>> request = requests.get('http://HOST:PORT/movies?limit=1000')
>>> request.json()
{'Movies': [{'imdbRating': '8.1', 'metascore': '88', 'rating': 4.6, 'id': 3, 'title': 'Donnie Darko'}, {'imdbRating': '9.0', 'metascore': '82', 'rating': 3.0, 'id': 2, 'title': 'The Dark Knight'}, {'imdbRating': '8.3', 'metascore': '70', 'rating': 4.2, 'id': 1, 'title': 'Batman Begins'}]}
### GET (by id)

>>> request = requests.get('http://HOST:PORT/movies/3?limit=1000')
>>> request.json()
{'imdbRating': '8.1', 'metascore': '88', 'rating': 4.3, 'id': 3, 'title': 'Donnie Darko'}
```
