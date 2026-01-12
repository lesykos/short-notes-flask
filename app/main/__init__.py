from flask import Blueprint

# Create a blueprint object main,
# with args:
#   name (main here),
#   __name__ - special variable,
#       which holds the name of the current Python module.
main = Blueprint("main", __name__)

from app.main import routes, errors
