from dateutil import parser
from flask import *
from functools import wraps
import time
from datetime import datetime
from workerfunctions import update_status
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
        status = r.hget(friend['id'], 'status')
        if status is None:
            friend['status'] = 1 #Yellow - unknown
        else:
            friend['status'] = int(status)
        pass
        friend['status_time'] = int(r.hget(friend['id'], 'status_time') or -1)

    return jsonify(user)

@blueprint.route('/post/<user_id>', methods=["POST"])
@jsonp
def post_values(user_id):
    silent = request.form['silent']
    accelerometer = request.form['accelerometer']
    on_call = request.form['onCall']
    next_alarm_string = request.form.get('nextAlarm', "")

    if next_alarm_string == "":
        next_alarm = 0
    else:
        try:
            next_alarm = (parser.parse(next_alarm_string) - datetime.now()).total_seconds()/60
        except ValueError:
            next_alarm = 0

    r = Redis()
    r.hmset(user_id, {'silent': silent, 'accelerometer': accelerometer, 'on_call': on_call, 'next_alarm': next_alarm})
    job = Queue(connection=r).enqueue(update_status, user_id)
    return "success"


@blueprint.route('/post/<user_id>/channel', methods=["POST"])
@jsonp
def post_value(user_id):
    try:
        channelName = request.json['channel']
        value = request.json['value']
    except TypeError:
        channelName = request.form['channel']
        value = request.form['value']

    if channelName == "chrome":
        value = is_productive(value)
        if value < 0:
            # Couldn't classify
            return

    r = Redis()
    r.hset(user_id, channelName, value)
    Queue(connection=r).enqueue(update_status, user_id)

    return "Success"

unproductiveWebsites = ["reddit", "facebook", "twitter"]
productiveWebsites = ["google", "github", "gmail"]

def is_productive(website):
    print website
    unproductive = len([w for w in unproductiveWebsites if website.find(w) >= 0]) > 0
    productive = len([w for w in unproductiveWebsites if website.find(w) >= 0]) > 0

    if productive:
        return 0
    elif unproductive:
        return 1
    else:
        return -1
