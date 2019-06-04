import binascii
import hashlib
import uuid
import helpers


def get_token_from_header(request):
    if request is not None and request.headers is not None and 'Authorization' in request.headers:
        authorization_info = request.headers['Authorization'].split(' ')
        if authorization_info.count() > 1 and (
                authorization_info[0] == 'Token' or authorization_info[0] == 'Bearer'):
            return authorization_info[1]

    return None


def validate_password(password, password_hash, password_salt):
    if not (helpers.is_blank(password) or helpers.is_blank(password_hash) or helpers.is_blank(password_salt)):
        validate_hash = \
            binascii.hexlify(hashlib.pbkdf2_hmac("sha512", str.encode(password), str.encode(password_salt), 10000))
        return validate_hash and validate_hash == password_hash

    return False


def encrypted_password(password):
    if not helpers.is_blank(password):
        password_salt = uuid.uuid4().hex
        password_hash = \
            binascii.hexlify(hashlib.pbkdf2_hmac("sha512", str.encode(password), str.encode(password_salt), 10000))

        return {'salt': password_salt, 'hash': password_hash}

    return None
