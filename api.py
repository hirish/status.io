from flask import Blueprint, jsonify

blueprint = Blueprint('api', __name__)

@blueprint.route('/get/<user_id>')
def get_user(user_id):
    user = { 'user_id': user_id, 'name': 'James' }
    return jsonify(user = user)
