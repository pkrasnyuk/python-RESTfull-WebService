from flask import Flask, Blueprint, redirect
from flask_restplus import Api
from flask_cors import CORS
from app_core import config, seed
from endpoints import users_endpoint


app = Flask(__name__)
CORS(app)

__api_prefix = '/api'
__authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'authorization'
    }
}

blueprint = Blueprint('api', __name__, url_prefix=__api_prefix)
api = Api(blueprint, version='1.0', title='Python WebServer API', description='Example of Python WebServer API',
          authorizations=__authorizations, security='apikey')
api.add_namespace(users_endpoint.instance)
app.register_blueprint(blueprint)


@app.route('/')
def core():
    return redirect(__api_prefix)


def main():
    if config is not None:
        seed()
        app.run(debug=True, host=config.host, port=config.port)


if __name__ == '__main__':
    main()
