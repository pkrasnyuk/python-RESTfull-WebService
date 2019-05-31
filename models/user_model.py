from user_type import UserType
import app_security
import helpers
from cerberus import Validator


class User:
    __id = None
    __name = None
    __email = None
    __passwordHash = None
    __passwordSalt = None
    __type = UserType.Developer

    __name_schema = {'type': 'string', 'required': True, 'empty': False}
    __email_schema = {'type': 'string', 'required': True, 'empty': False,
                      'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'}
    __password_schema = {'type': 'string', 'required': True, 'empty': False}
    __type_schema = {'type': 'integer', 'required': True, 'empty': False, 'min': UserType.Developer,
                     'max': UserType.Client}

    __schema_put = {'name': __name_schema, 'email': __email_schema, "type": __type_schema}
    __schema_post = {'name': __name_schema, 'email': __email_schema, "type": __type_schema,
                     "password": __password_schema}

    __validator = Validator()

    def __init__(self, user_id=None, name=None, email=None, password_hash=None, password_salt=None,
                 user_type=UserType.Developer):
        self.__id = user_id
        self.name = name
        self.email = email
        self.__passwordHash = password_hash
        self.__passwordSalt = password_salt
        self.type = user_type

    def __str__(self):
        return " Id: {0}\n User Name: {1}\n Email: {2}\n Password Hash: {3}\n Password Salt: {4}\n Type: {5}"\
            .format(self.__id, self.name, self.email, self.__passwordHash, self.__passwordSalt, self.type)

    @classmethod
    def instance(cls, name, email, password, user_type):
        user_password_hash = None
        user_password_salt = None
        if not helpers.is_blank(password):
            user_security_properties = app_security.encrypted_password(password)
            if user_security_properties is not None:
                if 'hash' in user_security_properties and not helpers.is_blank(user_security_properties['hash']):
                    user_password_hash = user_security_properties['hash']
                if 'salt' in user_security_properties and not helpers.is_blank(user_security_properties['salt']):
                    user_password_salt = user_security_properties['salt']

        return cls(name=name, email=email, password_hash=user_password_hash, password_salt=user_password_salt,
                   user_type=user_type)

    @classmethod
    def deserializable(cls, json_object):
        user_id = json_object['_id'] if json_object is not None and '_id' in json_object else None
        user_name = json_object['name'] if json_object is not None and 'name' in json_object else None
        user_email = json_object['email'] if json_object is not None and 'email' in json_object else None
        user_password_hash = json_object['passwordHash'] if json_object is not None and 'passwordHash' in json_object \
            else None
        user_password_salt = json_object['passwordSalt'] if json_object is not None and 'passwordSalt' in json_object \
            else None
        user_type = json_object['type'] if json_object is not None and 'type' in json_object else UserType.Developer

        return cls(user_id=user_id, name=user_name, email=user_email, password_hash=user_password_hash,
                   password_salt=user_password_salt, user_type=user_type)

    @classmethod
    def post_instance(cls, json_object):
        validation_result = cls.__validator.validate(document=json_object, schema=cls.__schema_post)
        if not validation_result:
            raise ValueError(cls.__validator.errors)

        user_name = json_object['name'] if json_object is not None and 'name' in json_object else None
        user_email = json_object['email'] if json_object is not None and 'email' in json_object else None
        user_password = json_object['password'] if json_object is not None and 'password' in json_object \
            else None
        user_type = json_object['type'] if json_object is not None and 'type' in json_object else UserType.Developer

        return cls.instance(name=user_name, email=user_email, password=user_password, user_type=user_type)

    def update(self, user, json_object):
        validation_result = self.__validator.validate(document=json_object, schema=self.__schema_put)
        if not validation_result:
            raise ValueError(self.__validator.errors)

        if json_object is not None and 'name' in json_object:
            user.name = json_object['name']
        if json_object is not None and 'email' in json_object:
            user.email = json_object['email']
        if json_object is not None and 'type' in json_object:
            user.type = json_object['type']
        return user

    def serializable(self):
        return {
            'name': self.name,
            'email': self.email,
            'passwordHash': self.__passwordHash,
            'passwordSalt': self.__passwordSalt,
            'type': self.type
        }

    def to_view_model(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'type': self.type
        } if self is not None else {}

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def password_hash(self):
        return self.__passwordHash

    @property
    def password_salt(self):
        return self.__passwordSalt

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value
