from flask import Flask

from models import db

import os
import api
import main

app = Flask(__name__)

_basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(_basedir, 'app_dev.db')

db.init_app(app)

app.register_blueprint(api.blueprint)
app.register_blueprint(main.blueprint)

# run the application!
if __name__ == '__main__':
     # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
