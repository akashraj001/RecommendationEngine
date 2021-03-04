# flask packages
from flask import Flask, app
from flask_restful import Api

# local packages
from recomEngine.src.main.apis import routes

# default mongodb configuration
default_config = {'MONGODB_SETTINGS': {
    'db': 'bighaat',
    'host': '20.185.77.19',
    'port': 27017,
    'username': 'root',
    'password': '78jS7cHZWv',
    'authentication_source': 'admin'}}


def get_flask_app(config: dict = None) -> app.Flask:
    """
    Initializes Flask app with given configuration.
    Main entry point for wsgi (gunicorn) server.
    :param config: Configuration dictionary
    :return: app
    """
    # init flask
    flask_app = Flask(__name__)

    # configure app mongo
    # config = default_config if config is None else config
    # flask_app.config.update(config)

    # init api and routes
    api = Api(app=flask_app)
    routes.create_routes(api=api)

    # init mongoengine mongo
    # db = MongoEngine(app=flask_app)

    return flask_app


if __name__ == '__main__':
    # Main entry point when run in stand-alone mode.
    app = get_flask_app()
    app.run(debug=True)
