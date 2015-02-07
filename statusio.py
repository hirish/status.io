from flask import Flask

import api

app = Flask(__name__)
app.register_blueprint(api.blueprint)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
