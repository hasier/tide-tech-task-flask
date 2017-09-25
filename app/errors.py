# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from app.utils import jsonify


logger = logging.getLogger(__name__)


class CoreError(Exception):
    def __init__(self, code, msg, key):
        super(CoreError, self).__init__(msg)
        self.key = key
        self.code = code


class AuthError(CoreError):
    def __init__(self, msg='Unauthorized', key='auth_error', **kwargs):
        super(AuthError, self).__init__(401, msg, key, **kwargs)


def setup_errors(app):
    @app.errorhandler(CoreError)
    def core_error(err):
        return jsonify(dict(key=err.key, message=err.message), status_code=err.code)

    @app.errorhandler(404)
    def core_error(err):
        return jsonify(dict(key='url_not_found_error', message='URL not found'), status_code=404)

    @app.errorhandler(Exception)
    def server_error(err):
        logger.exception(err, exc_info=True)
        return jsonify(dict(key='internal_server_error', message='Internal server error'), status_code=500)

