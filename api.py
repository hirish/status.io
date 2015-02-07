from flask import *
from functools import wraps

from models import User

blueprint = Blueprint('api', __name__)

def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function

@blueprint.route('/get/<user_id>')
@jsonp
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user = user.output())
