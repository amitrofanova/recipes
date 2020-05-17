from flask import Blueprint

# TODO if you add a template_folder='templates' argument to the Blueprint() constructor, you can then store the
# blueprint's templates in app/errors/templates
bp = Blueprint('errors', __name__)

from app.errors import handlers
