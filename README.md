# Ratings Aggregator API

Thanks for taking the time to take our challenge. We're hoping that you can follow a few guidelines and deliver a simple, working API that conforms to the interface set forth below.

## Goals

We're hoping to learn a bit more about your personal dev style and preferences, so feel free to choose the language, libraries, and any other weapons of choice. As a backend engineer in our organization, we find ourselves relying on a lot of PaaS (platforms as a service), which means a lot of integration with 3rd party APIs. In the spirit of working with a 3rd party API, this challenge focuses on building an API which acts as a Consumer of another API ([The Open Movie Database](https://www.omdbapi.com/)), and a Provider to a number of client-side apps.

The other half of the challenge (aside from getting it to work on your laptop!) is to provide human-readable deployment instructions or, as a bonus, actually deploy to a internet-accessible, public-facing endpoint.

This repo provides an initial starting point, so please fork and commit your work to your fork. Wherever you take it, or whether or not you use the files in this repo at all, is completely up to you.

## Instructions

Our users, much like the movie-watching public at large, are often faced with the question of: what should I watch next? While our services currently offer a curated selection of films and a number of ways you can look for stuff you haven't seen yet, let's look at the problem within the context of an imaginary service, that may or may not exist in the future, _TooManyFlix_, which offers a dizzying array of films. Users are allowed to post reviews and star ratings (1 to 5) already, but we want to be able to list them alongside other aggregate ratings from services like IMDb and Rotten Tomatoes.

We would like you to build an API that allows consumers to register a new movie `title`, with an associated combined user `rating`. When we subsequently request information about the same movie, we would like the API to return a `metascore` (Metacritic rating) and `imdbRating` for the movie.

#### A RESTful API

As a consumer of this API, I should be able to:

1. List all movies registered in the system (HTTP GET /movies)
2. Register a new movie (HTTP POST /movies), with a Title and Rating (combined user rating)
3. Update an existing movie registed in the system (HTTP PUT /movies)
4. Get details for a single movie registered in the system (HTTP GET /movies/123)

`swagger.yaml` sets forth the basic JSON contract that we would like the API to adhere to. If you've never used Swagger or the [Open API Spec](https://openapis.org/specification) before, go to http://editor.swagger.io/, paste in the contents of `swagger.yaml`, and it will generate some easy-to-follow documentation on the right-hand side

#### Integrating with a 3rd party

At this point, you have the RESTful endpoints above in a working state.

As a consumer of this API, I would now like the movie details call to return aggregate ratings. These ratings will be provided by the Open Movie Database, which can be found here: https://www.omdbapi.com/

For example, if `HTTP GET /movies/1` returned info about the movie "Donnie Darko", based on http://www.omdbapi.com/?t=donnie+darko&y=&plot=short&r=json, we would expect the response to look something like:

```json
{
    "id": 1,
    "title": "Donnie Darko",
    "rating": 4.0,
    "metascore": "71",
    "imdbRating": "8.1"
}
```

### Requirements

* Use any language, server, tools of your choice, but your API must be able to communicate over HTTP
* JSON and REST are both optional but highly recommended (be prepared to explain your choice if not!)
* Provide human-readable deployment instructions on how to deploy the application to a fresh Linux machine or a service like Heroku
* Actually deploying to a publically-accessible endpoint is a plus!
* To limit the scope of this challenge, authentication and authorization are both outside of scope
