"""
This script creates a RESTful API with a Redis database to manage a list of movies.
Each movie is stored as a key-value pair in the Redis database,
where the key is 'movie:{id}' and the value is a JSON string.
Each movie object has two properties: 'title' and 'year'.
"""

import json

import redis
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse

app = Flask('MovieAPI')  # creating a Flask application
api = Api(app)  # creating a RESTful API

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)  # Redis server

# creating a parser for requests
parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('year', required=True, type=int)


class MovieList(Resource):
    """
    A class for a list of movies.
    Inherits from Flask-RESTful Resource.
    """

    def get(self):
        movies = {}
        for key in r.keys('movie:*'):
            movies[key.split(':')[1]] = json.loads(r.get(key))
        return movies

    def post(self):
        args = parser.parse_args()
        new_movie_id = r.incr('id')
        new_movie = {
            'title': args['title'],
            'year': args['year']
        }
        r.set(f'movie:{new_movie_id}', json.dumps(new_movie))
        return {new_movie_id: new_movie}, 201


class Movie(Resource):
    """
    A class for an individual movie.
    Inherits from Flask-RESTful Resource.
    """

    @staticmethod
    def movie_error(movie_id):
        if not r.exists(f'movie:{movie_id}'):
            abort(404, message=f'Movie with id {movie_id} not found.')

    def get(self, movie_id):
        self.movie_error(movie_id)
        movie = json.loads(r.get(f'movie:{movie_id}'))
        return {movie_id: movie}, 200

    def put(self, movie_id):
        self.movie_error(movie_id)
        args = parser.parse_args()
        updated_movie = {
            'title': args['title'],
            'year': args['year']
        }
        r.set(f'movie:{movie_id}', json.dumps(updated_movie))  # update movie
        return {movie_id: updated_movie}, 200


# Adding routes
api.add_resource(MovieList, '/movies/')
api.add_resource(Movie, '/movies/<int:movie_id>/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
