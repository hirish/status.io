from flask import Blueprint, jsonify

from models import User

blueprint = Blueprint('api', __name__)

@blueprint.route('/get/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user = user.output())
