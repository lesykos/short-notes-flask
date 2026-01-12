# To make the app project directory a Python package,
# we create a special __init__.py file inside of it,
# which marks directories as Python packages.
import os
from flask import Flask
from dotenv import load_dotenv
from supabase import create_client, Client
from config import config

# read variables from a .env file and set them in os.environ
load_dotenv()

supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


# Flask factory function,
# is a function we use to set and create
# the Flask application instance
# where we link all our Flask blueprints together.
def create_app(config_name):
    # Create an application instance - an object of class Flask
    app = Flask(__name__)

    # Load the configuration from the config module
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize Flask extensions here
    # ... for example, database, login manager, etc.

    # here all our Flask components (blueprints)
    # are combined into one application.
    from app.main import main as main_blueprint
    from app.notes import notes as notes_blueprint
    from app.tags import tags as tags_blueprint
    from app.auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(notes_blueprint)
    app.register_blueprint(tags_blueprint)
    app.register_blueprint(auth_blueprint)

    app.config["SUPABASE_CLIENT"] = supabase

    return app
