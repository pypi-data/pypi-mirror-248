import logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

class ValidationError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        logging.error('An error occurred: %s', str(msg))

    def __str__(self):
        return self.msg