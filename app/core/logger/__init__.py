from flask.ext.login import current_user
from flask import request
from app import app
import logging


class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        log_record.url = request.path
        log_record.method = request.method
        log_record.ip = request.environ.get("REMOTE_ADDR")
        log_record.user_id = -1 if current_user.is_anonymous() else current_user.get_id()

        return True


context_provider = ContextualFilter()
app.logger.addFilter(context_provider)
del app.logger.handlers[:]

handler = logging.StreamHandler()

log_format = "%(asctime)s\t%(levelname)s\t%(user_id)s\t"+\
             "%(ip)s\t%(method)s\t%(url)s\t%(message)s"
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

app.logger.addHandler(handler)

from logging import ERROR
from logging.handlers import TimedRotatingFileHandler

# Only set up a file handler if we know where to put the logs
if app.config.get("ERROR_LOG_PATH"):

    # Create one file for each day. Delete logs over 7 days old.
    file_handler = TimedRotatingFileHandler(
            app.config["ERROR_LOG_PATH"],
            when="D",
            backupCount=7
            )

    # Use a multi-line format for this logger, for easier scanning
    file_formatter = logging.Formatter('''
    Time: %(asctime)s
    Level: %(levelname)s
    Method: %(method)s
    Path: %(url)s
    IP: %(ip)s
    User ID: %(user_id)s
    Message: %(message)s
    ---------------------''')

    # Filter out all log messages that are lower than Error.
    file_handler.setLevel(ERROR)

    file_handler.addFormatter(file_formatter)
    app.logger.addHandler(file_handler)
