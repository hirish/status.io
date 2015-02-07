from flask import *
from functools import wraps

from models import *

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
    json

@blueprint.route('/post/<user_id>', methods=["POST"])
@jsonp
def post_values(user_id):
    raw_data = request.json['data']
    values = raw_data[::2]
    keys = raw_data[1::2]

    user = User.query.get(user_id)

    for value, key in zip(values, keys):
        db.session.add(DataPoint(value, key, user))
        db.session.commit()
    
    return "success"

@blueprint.route('/datapoints')
def all_datapoints():
    datapoints = DataPoint.query.all()
    return jsonify(datapoints = [datapoint.output() for datapoint in datapoints])
