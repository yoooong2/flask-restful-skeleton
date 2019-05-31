import os

from flask import Flask

def create_app(test_config=None):
    """Create and configure the app."""
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )    
    load_config(app, test_config) 
    init_instance_folder(app) 
    registes_blueprints(app)
        
    return app


def load_config(app, test_config): 
    """Load the application's config"""

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


def init_instance_folder(app):
    """Ensure the instance folder exists."""

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass        


def registes_blueprints(app):
    """Registes the blueprint to the application."""

    from .blueprint import index
    app.register_blueprint(index.bp)