import logging


class Configuration():
    def __init__(self):
        self.__set_up_logging_config()

    def __set_up_logging_config(self):
        logging.basicConfig(
            filename='conductor_python_client.log',
            filemode='w',
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
