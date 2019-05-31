import app_config
import app_security
import db_access
import helpers

__CONFIG_FILE = "config.json"
config = app_config.load_configuration(__CONFIG_FILE)

logger = helpers.Logger(config.logging_name, config.logging_file).logger_instance
security_service = app_security.Security(config.private_key, config.token_expiry, logger)
db = db_access.DbAccess(config.connection_string, config.db_name, logger).db
