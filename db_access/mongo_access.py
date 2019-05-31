from pymongo import MongoClient
import helpers


class DbAccess:
    __db_connection_string = None
    __db_name = None
    __logger = None

    __client = None
    __db = None

    def __init__(self, connection_string, db_name, logger):
        self.__db_connection_string = connection_string
        self.__db_name = db_name
        self.__logger = logger

        try:
            if not helpers.is_blank(self.__db_connection_string):
                self.__client = MongoClient(self.__db_connection_string)

            if self.__client is not None and not helpers.is_blank(self.__db_name):
                self.__db = self.__client[self.__db_name]
        except Exception as e:
            if self.__logger is not None:
                self.__logger.error(e.message)

    @property
    def db(self):
        return self.__db
