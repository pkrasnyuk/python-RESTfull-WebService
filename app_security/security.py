import datetime
import jwt
from flask_httpauth import HTTPTokenAuth
from app_security.security_helper import *
import helpers


class Security:
    __security_private_key = None
    __security_token_expiry = 0
    __logger = None

    def __init__(self, private_key, token_expiry, logger):
        self.__security_private_key = private_key
        self.__security_token_expiry = token_expiry
        self.__logger = logger

    def generate_token(self, user):
        if user is not None and not helpers.is_blank(self.__security_private_key) and self.__security_token_expiry > 0:
            return jwt.encode(payload={
                "id": str(user.id),
                "email": user.email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=self.__security_token_expiry)},
                key=self.__security_private_key, algorithm='HS256')

        return None

    def verify_token(self, token):
        if not (helpers.is_blank(token) or helpers.is_blank(self.__security_private_key)):
            try:
                result = jwt.decode(jwt=token, key=self.__security_private_key, verify=True,
                                           algorithms=['HS256'])
                return result is not None
            except jwt.ExpiredSignatureError as e:
                if self.__logger is not None:
                    self.__logger.error(e)
                print(e)

        return False

    def validate_authenticate_request(self, request):
        code = 200
        message = ""

        if request is not None:
            token = get_token_from_header(request)
            if helpers.is_blank(token):
                code = 404
                message = "Incorrect request"

            if not self.verify_token(token):
                code = 401
                message = "You are unauthorized for this operation"

        else:
            code = 404
            message = "Incorrect request"

        return {'code': code, 'message': message}

    @staticmethod
    def authentication_init():
        return HTTPTokenAuth('Bearer')