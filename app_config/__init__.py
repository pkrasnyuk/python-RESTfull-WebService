import json
import os
from app_config.config import Config


def load_configuration(config_file_path):
    if config_file_path and os.path.isfile(config_file_path):
        with open(config_file_path, "r") as config_file:
            try:
                load_result = json.dumps(json.load(config_file))
                return __obj_creator(json.loads(load_result))
            except Exception as e:
                print(e)

    return __obj_creator(None)


def __obj_creator(json_object):
    config_host = None
    config_port = 0
    config_connection_string = None
    config_db_name = None
    config_security_private_key = None
    config_token_expiry = 0
    config_logging_name = None
    config_logging_file = None

    if json_object is not None:

        if 'app' in json_object and 'host' in json_object['app']:
            config_host = json_object['app']['host']

        if 'app' in json_object and 'port' in json_object['app']:
            config_port = int(json_object['app']['port'])

        if 'db' in json_object and 'connectionString' in json_object['db']:
            config_connection_string = json_object['db']['connectionString']

        if 'db' in json_object and 'dbName' in json_object['db']:
            config_db_name = json_object['db']['dbName']

        if 'security' in json_object and 'privateKey' in json_object['security']:
            config_security_private_key = json_object['security']['privateKey']

        if 'security' in json_object and 'tokenExpiry' in json_object['security']:
            config_token_expiry = json_object['security']['tokenExpiry']

        if 'logging' in json_object and 'loggingName' in json_object['logging']:
            config_logging_name = json_object['logging']['loggingName']

        if 'logging' in json_object and 'loggingFile' in json_object['logging']:
            config_logging_file = json_object['logging']['loggingFile']

        return Config(
            host=config_host,
            port=config_port,
            connection_string=config_connection_string,
            db_name=config_db_name,
            private_key=config_security_private_key,
            token_expiry=config_token_expiry,
            logging_name=config_logging_name,
            logging_file=config_logging_file)


def __main():
    config_file_path = "../config.json"
    print(load_configuration(config_file_path))


if __name__ == '__main__':
    __main()
