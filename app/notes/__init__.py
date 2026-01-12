from flask import Blueprint

# Create a blueprint object notes
notes = Blueprint("notes", __name__, url_prefix="/notes")

from app.notes import routes
