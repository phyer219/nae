import logging
from .util import make_dir_exist


class Logger:
    def __init__(self, log_name, log_file, log_level=logging.INFO,
                 stdout=True):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            formatter = logging.Formatter('''%(asctime)s - %(levelname)s from %(name)s: %(message)s''')
            make_dir_exist(log_file)
            fh = logging.FileHandler(log_file)
            fh.setLevel(log_level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

            if stdout:
                ch = logging.StreamHandler()
                ch.setLevel(log_level)
                ch.setFormatter(formatter)
                self.logger.addHandler(ch)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
