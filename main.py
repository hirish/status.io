from flask import Blueprint, send_file

blueprint = Blueprint('main', __name__)

@blueprint.route('/')
def hello_world():
    return send_file('static/index.html')
