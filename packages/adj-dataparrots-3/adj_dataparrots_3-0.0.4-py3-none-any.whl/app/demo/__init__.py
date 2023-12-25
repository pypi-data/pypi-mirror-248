from flask import Blueprint

bp = Blueprint('demo', __name__, url_prefix='/api/demo')

from . import routes
