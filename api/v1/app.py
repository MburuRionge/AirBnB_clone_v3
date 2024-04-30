#!/usr/bin/python3

"""Flask app that intergartes with Airbnb static HTML Template"""

from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
from api.v1.views import app_views
from flask_cors import CORS, cross_origin
from flasgger import Swagger
import os
from werkzeug.exceptions import HTTPException


# global Flask applicaton variable - app
app = Flask(__name__)
swagger = Swagger(app)

# global strict slashes
app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# Cross-Origin Resource sharing
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# app_views BluePrint defined in apiv1.views
app.register_blueprint(app_views)


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    after each reqiest, it calls .close() i.e .remove() on the current
    SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """ if global error handler fails it handles 404 """
    code = exeption.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(400)
def handle400(exception):
    """handles 400 errors incase the global error handler fails"""
    code = exception.__str__().split()[0]
    description = exception.description
    message {'error': description}
    return make_respone(jsonify(message), code)


@app.errorhandler(Exception)
def global_error_handler(err):
    """ global route to handle all error status codes """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'Not found':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """ updates HTTPException class with custom error function """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == '__main__':
    """ main flask app """
    # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port=port)
