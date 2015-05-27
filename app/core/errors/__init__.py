from app.core import logger, exceptions
from os.path import join
from flask import send_from_directory, jsonify
from app import app, auth


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
            join(app.root_path, 'static'),
            'ico/favicon.ico'
            )

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
            'return_code': 404,
            'message': 'This is not the page you are looking for.'
            }), 404

@app.errorhandler(400)
def key_error(e):
    app.logger.warning('Invalid request resulted in KeyError', exc_info=e)
    return jsonify({
            'return_code': 400,
            'message': e
            }), 400

@auth.error_handler
def authorized():
    app.logger.warning('Invalid Authorization')
    resp = jsonify({
            'return_code': 401,
            'message': 'Invalid Authorization'
            })
    resp.status_code = 401
    return resp

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.warning(
            'An unhandled exception is being displayed to the end user',
            exc_info=e
            )
    return jsonify({
            'return_code': 500,
            'message': e
            }), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.warning(
            'An unhandled exception is being displayed to the end user',
            exc_info=e
            )
    return jsonify({
            'return_code': 500,
            'message': e
            }), 500

@app.before_request
def log_entry():
    app.logger.debug("Handling request")

@app.teardown_request
def log_exit(exc):
    app.logger.debug("Finished handling request", exc_info=exc)

