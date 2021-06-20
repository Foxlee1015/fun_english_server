from flask import Blueprint
from flask_restplus import Api
import jwt

from .verbs import api as verbs
from .logs import api as logs
from .sessions import api as sessions
from .tokens import api as tokens
from .users import api as users


blueprint = Blueprint('api', __name__)
api = Api(
    blueprint,
    title='Fun English API',
    version='1.0',
    description='A description'
)

api.add_namespace(verbs)
api.add_namespace(logs)
api.add_namespace(sessions)
api.add_namespace(users)
api.add_namespace(tokens)