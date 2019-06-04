import app_config
import app_security
import db_access
import helpers
import models

__CONFIG_FILE = "config.json"
config = app_config.load_configuration(__CONFIG_FILE)

logger = helpers.Logger(config.logging_name, config.logging_file).logger_instance
security_service = app_security.Security(config.private_key, config.token_expiry, logger)
db = db_access.DbAccess(config.connection_string, config.db_name, logger).db


def seed():
    admin_email = "admin@mail.com"
    db_admin = db.users.find_one({'email': admin_email})
    if db_admin is None:
        user = models.User.instance("admin", admin_email, "admin", models.UserType.Manager.value)
        db.users.insert_one(user.serializable())
