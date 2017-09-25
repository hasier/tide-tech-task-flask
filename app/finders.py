# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from app import features, users


USER_TOKEN_FORMAT = 'token:{}'
USER_FEATURES_FORMAT = 'features:user:{}'


class UserFinder(object):
    @classmethod
    def get_user_id_from_token(cls, token):
        '''
        Returns the user ID associated to the given token, if any.

        :param token: The auth token to check.
        :return: Integer user ID if it is a correct token; None otherwise.
        '''
        return users.get(USER_TOKEN_FORMAT.format(token))


class FeatureFinder(object):
    @classmethod
    def get_active_features(cls, user_id=None):
        '''
        Returns the globally active features, as well as the particular ones for a user.

        :param user_id: (Optional) If given, appends to the globally available features the ones active for this user.
        :return: List with all the active features.
        '''
        feats = features.smembers('global_features')
        if user_id is not None:
            feats |= features.sinter('active_features', USER_FEATURES_FORMAT.format(user_id))
        return list(feats)

