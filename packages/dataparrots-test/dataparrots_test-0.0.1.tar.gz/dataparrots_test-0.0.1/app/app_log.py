from config import Config
import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class app_log:
    _logger = None
    
    @staticmethod
    def logger():
        if app_log._logger == None:
            app_log._logger = logging.getLogger()
            if not os.path.exists(Config.LOG_DIR):
                os.mkdir(Config.LOG_DIR)
            file_handler = RotatingFileHandler(Config.LOG_DIR+'/ailog.log', maxBytes=102400, backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
            file_handler.setLevel(logging.INFO)
            app_log._logger.addHandler(file_handler)
            app_log._logger.setLevel(logging.INFO)

        return app_log._logger

    @staticmethod
    def errorHandler():
        if not os.path.exists(Config.LOG_DIR):
            os.mkdir(Config.LOG_DIR)
        formatter = logging.Formatter(
            "[%(asctime)s][%(pathname)s.%(funcName)s:%(lineno)d][%(levelname)s] - %(message)s")
        handler = TimedRotatingFileHandler(
            Config.LOG_DIR+"/error.log", when="D", interval=1, backupCount=15,
            encoding="UTF-8", delay=False, utc=True)
        handler.setFormatter(formatter)
        handler.setLevel(logging.WARNING)
        return handler
