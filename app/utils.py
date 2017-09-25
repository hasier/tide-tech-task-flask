# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from flask.json import jsonify as flask_jsonify


def jsonify(data, status_code=200):
    '''
    Convenience function to serialize a dict/list structure into a Response object
    and directly append a status code to it.

    :param data: a dictionary or list object to include in the Response.
    :param int status_code: (Optional) The intended status code for the Response. 200 by default.
    :return: Flask Response object ready to return from the endpoint.
    '''
    res = flask_jsonify(data)
    res.status_code = status_code
    return res

