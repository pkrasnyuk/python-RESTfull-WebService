import time

import helpers
import models
from app_security.security import Security
from app_security.security_helper import encrypted_password, validate_password


def __main():
    logger = helpers.Logger("app_logger", "../app.log").logger_instance
    app_security = Security("39LvDSm45vjYOh90", 30, logger)

    password = "test"
    res = encrypted_password(password)
    print(res)
    validate_status = validate_password(password, res["hash"], res["salt"])
    print(validate_status)

    user = models.User("pktest", "pktest@mail.com", "test", models.UserType.Manager)
    token = app_security.generate_token(user)
    print(token)

    time.sleep(32)

    verification_result = app_security.verify_token(token)
    print(verification_result)


if __name__ == "__main__":
    __main()
