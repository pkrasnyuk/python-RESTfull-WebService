import logging
import helpers


class Logger:
    __logging_name = None
    __logging_file = None
    __logger = None

    def __init__(self, logging_name, logging_file):
        self.__logging_name = logging_name
        self.__logging_file = logging_file

        if not (helpers.is_blank(self.__logging_name) or helpers.is_blank(self.__logging_file)):

            self.__logger = logging.getLogger(self.__logging_name)
            self.__logger.setLevel(logging.DEBUG)

            ch = logging.FileHandler(self.__logging_file)
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.__logger.addHandler(ch)

    @property
    def logger_instance(self):
        return self.__logger
