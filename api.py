from flask import *
from functools import wraps
from workerfunctions import is_free
from redis import Redis
from rq import Queue

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
    user = User.query.get(user_id).output()
    r = Redis()
    for friend in user['friends']:
        status = r.get(friend['id'])
        if status is None:
            friend['status'] = 1 #Yellow - unknown
        else:
            friend['status'] = int(status)
        pass

    return jsonify(user)

@blueprint.route('/post/<user_id>', methods=["POST"])
@jsonp
def post_values(user_id):
    location = request.json['location']
    accelerometer = request.json['accelerometer']
    ringer = request.json['ringer']
    call = request.json['call']
    calendar = request.json['calendar']

    job = Queue(connection=Redis()).enqueue(is_free, user_id, location, accelerometer, ringer, call, calendar)

    # user = User.query.get(user_id)

    # for value, key in zip(values, keys):
    #     db.session.add(DataPoint(value, key, user))
    #     db.session.commit()
    
    return "success"

@blueprint.route('/datapoints')
def all_datapoints():
    datapoints = DataPoint.query.all()
    return jsonify([datapoint.output() for datapoint in datapoints])
