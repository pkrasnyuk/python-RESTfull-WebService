class Config:
    __host = None
    __port = 0
    __connectionString = None
    __dbName = None
    __privateKey = None
    __tokenExpiry = 0
    __loggingName = None
    __loggingFile = None

    def __init__(self, host, port, connection_string, db_name, private_key, token_expiry, logging_name, logging_file):
        self.__host = host
        self.__port = port
        self.__connectionString = connection_string
        self.__dbName = db_name
        self.__privateKey = private_key
        self.__tokenExpiry = token_expiry
        self.__loggingName = logging_name
        self.__loggingFile = logging_file

    def __str__(self):
        return (
            " Host: {0}\n Port: {1}\n Connection String: {2}\n DB Name: {3}\n Private Key: {4}"
            "\n Token Expiry: {5}\n Logging Name: {6}\n Logging file: {7}".format(
                self.__host,
                self.__port,
                self.__connectionString,
                self.__dbName,
                self.__privateKey,
                self.__tokenExpiry,
                self.__loggingName,
                self.__loggingFile,
            )
        )

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def connection_string(self):
        return self.__connectionString

    @property
    def db_name(self):
        return self.__dbName

    @property
    def private_key(self):
        return self.__privateKey

    @property
    def token_expiry(self):
        return self.__tokenExpiry

    @property
    def logging_name(self):
        return self.__loggingName

    @property
    def logging_file(self):
        return self.__loggingFile
