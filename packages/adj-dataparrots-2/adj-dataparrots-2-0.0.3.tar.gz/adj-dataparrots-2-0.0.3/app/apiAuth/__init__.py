from flask import Blueprint

bp = Blueprint('apiAuth', __name__, url_prefix='/api/auth')

from . import routes