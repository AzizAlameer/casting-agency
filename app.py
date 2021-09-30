import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import requires_auth, AuthError
from models import Movie, Actor, setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'GET, POST, PATCH, DELETE, OPTION')
        return response

    @app.route('/')
    def index():
        return jsonify({
            'message': 'healthy and working'
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(f):

        try:

            movies = Movie.query.all()
            movies_format = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movies': movies_format
            }), 200

        except BaseException:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(f):
        data = request.get_json()
        if data is None:
            abort(400)
        title = data.get('title', None)
        release_date = data.get('release_date', None)

        if title is None or release_date is None:
            abort(400)
        movie = Movie(title=title, release_date=release_date)

        try:
            movie.insert()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 201
        except BaseException:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(f, id):
        data = request.get_json()
        if data is None:
            abort(400)
        title = data.get('title', None)
        release_date = data.get('release_date', None)

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        if title is None or release_date is None:
            abort(400)

        movie.title = title
        movie.release_date = release_date

        try:
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200
        except BaseException:
            abort(422)

    @app.route("/movies/<id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movies(f, id):
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)
        try:
            movie.delete()

            return jsonify({
                "success": True,
                "deleted": id
            }), 200
        except BaseException:
            abort(422)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(f):

        try:
            actors = Actor.query.all()

            actor_format = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actors': actor_format
            }), 200

        except BaseException:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(f):

        data = request.get_json()
        if data is None:
            abort(400)
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        actor = Actor(name=name, age=age, gender=gender)

        if name is None or age is None or gender is None:
            abort(400)

        try:
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201
        except BaseException:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(f, id):

        data = request.get_json()
        if data is None:
            abort(400)
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)

        if name is None or age is None or gender is None:
            abort(400)

        actor.name = name
        actor.age = age
        actor.gender = gender

        try:
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
        except BaseException:
            abort(422)

    @app.route("/actors/<id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actors(f, id):
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)
        try:
            actor.delete()

            return jsonify({
                "success": True,
                "deleted": id
            }), 200
        except BaseException:
            abort(422)

            # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
