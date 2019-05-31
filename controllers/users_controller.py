from flask import jsonify, Response, json
from app_core import security_service
from managers import UsersManager
from models import User
from helpers import common
from app_security import security_helper


class UsersController:
    __manager = None

    def __init__(self):
        self.__manager = UsersManager()

    def get_users(self):
        result = []
        users_collection = self.__manager.get_users() if self.__manager is not None else []
        for user in users_collection:
            result.append(user.to_view_model())
        return jsonify(result)

    def add_user(self, data):
        try:
            user = User.post_instance(data)

            if user is not None and not self.__manager.check_user_email(user.email):
                return Response(json.dumps({'message': 'An user must have unique email'}),
                                mimetype=u'application/json', status=422)

            status = self.__manager.add_user(user) if self.__manager is not None else False
            return Response(response=json.dumps({'message': 'User added successfully'}), mimetype=u'application/json',
                            status=201) if status else Response(json.dumps({'message': 'No user added'}),
                                                                mimetype=u'application/json', status=500)
        except ValueError as e:
            return Response(json.dumps({'message': e.message}), mimetype=u'application/json', status=422)
        except Exception:
            return Response(json.dumps({'message': 'Bad Request'}), mimetype=u'application/json', status=400)

    def get_user(self, user_id):
        result = self.__manager.get_user(user_id)
        return result.to_view_model() if result is not None else \
            Response(response=json.dumps({'message': 'User not found'}), mimetype=u'application/json', status=404)

    def delete_user(self, user_id):
        user = self.__manager.get_user(user_id)
        if user is not None:
            result = self.__manager.delete_user(user_id)
            return Response(response=json.dumps({'message': 'User removed successfully'}), mimetype=u'application/json',
                            status=200) if result else Response(response=json.dumps({'message': 'No user removed'}),
                                                                mimetype=u'application/json', status=500)
        else:
            return Response(response=json.dumps({'message': 'User not found'}), mimetype=u'application/json',
                            status=404)

    def update_user(self, user_id, data):
        try:
            user = self.__manager.get_user(user_id)
            if user is not None:
                user = User.update(user, data)

                if user is not None and not self.__manager.check_user_email(user.email):
                    return Response(json.dumps({'message': 'An user must have unique email'}),
                                    mimetype=u'application/json', status=422)

                result = self.__manager.update_user(user)
                return Response(response=json.dumps({'message': 'User updated successfully'}),
                                mimetype=u'application/json', status=200) if result else \
                    Response(response=json.dumps({'message': 'No user updated'}), mimetype=u'application/json',
                             status=500)
            else:
                return Response(response=json.dumps({'message': 'User not found'}), mimetype=u'application/json',
                                status=404)
        except ValueError as e:
            return Response(json.dumps({'message': e.message}), mimetype=u'application/json', status=422)
        except Exception:
            return Response(json.dumps({'message': 'Bad Request'}), mimetype=u'application/json', status=400)

    def login_user(self, data):
        if data is not None:
            user_email = data['email'] if data is not None and 'email' in data else None
            user_password = data['password'] if data is not None and 'password' in data else None
            if common.is_blank(user_email) or common.is_blank(user_password):
                return Response(response=json.dumps({'message': 'Incorrect request'}), mimetype=u'application/json',
                                status=500)
            else:
                user = self.__manager.get_user_by_email(user_email)
                message = 'An user with email={0} and password={1} not found'.format(user_email, user_password)
                if user is None:
                    return Response(response=json.dumps({'message': message}), mimetype=u'application/json', status=404)
                else:
                    is_password_valid = security_helper.validate_password(user_password, user.password_hash,
                                                                          user.password_salt)
                    if is_password_valid:
                        user_token = security_service.generate_token(user)
                        return Response(response=json.dumps({'token': 'Bearer {0}'.format(user_token)}),
                                        mimetype=u'application/json', status=200)
                    else:
                        return Response(response=json.dumps({'message': message}), mimetype=u'application/json',
                                        status=404)
            return True
        else:
            return Response(response=json.dumps({'message': 'Incorrect request'}), mimetype=u'application/json',
                            status=500)
