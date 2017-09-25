# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from flask import request

from app import app
from app.errors import AuthError
from app.finders import FeatureFinder, UserFinder
from app.utils import jsonify


@app.route('/features', methods=['GET'])
def features():
    user_id = None
    auth = request.authorization
    if auth:
        user_id = UserFinder.get_user_id_from_token(auth.password)
        if user_id is None:
            raise AuthError()
    features = FeatureFinder.get_active_features(user_id)
    return jsonify(dict(active_features=features))

