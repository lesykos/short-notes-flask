from flask import Blueprint

tags = Blueprint("tags", __name__, url_prefix="/tags")

from app.tags import routes
