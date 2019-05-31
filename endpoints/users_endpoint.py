from flask import request
from flask_restplus import Namespace, Resource, fields
import controllers
from app_core import security_service


auth = security_service.authentication_init()
users_controller = controllers.UsersController()

instance = Namespace('users', description='Operations related to users')

register_user_model = instance.model('register_user', {
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'type': fields.Integer(required=True, description='User type')
})

updated_user_model = instance.model('updated_user', {
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
    'type': fields.Integer(required=True, description='User type')
})


login_user_model = instance.model('login_user', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@auth.verify_token
def verify(token):
    return security_service.verify_token(token)


@instance.route('/')
class UsersCollection(Resource):
    @staticmethod
    def get():
        return users_controller.get_users()

    @staticmethod
    @instance.expect(register_user_model)
    @auth.login_required
    def post():
        return users_controller.add_user(request.json)


@instance.route('/<string:id>')
@instance.param('id', 'The user identifier')
class UserItem(Resource):
    @staticmethod
    def get(id):
        return users_controller.get_user(id)

    @staticmethod
    @auth.login_required
    def delete(id):
        return users_controller.delete_user(id)

    @staticmethod
    @instance.expect(updated_user_model)
    @auth.login_required
    def put(id):
        return users_controller.update_user(id, request.json)


@instance.route('/login')
class UserLogin(Resource):
    @staticmethod
    @instance.expect(login_user_model)
    def post():
        return users_controller.login_user(request.json)
