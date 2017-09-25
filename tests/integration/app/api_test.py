# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import pytest

from app import features, users
from app.finders import USER_FEATURES_FORMAT, USER_TOKEN_FORMAT
from tests.integration.utils import generate_authorization_string


@pytest.fixture
def global_features():
    feats = ['feature_1', 'feature_2']
    features.sadd('global_features', *feats)
    yield feats
    features.delete('global_features')


@pytest.fixture
def user():
    user_id = 7
    token = 'asdf'
    users.set(USER_TOKEN_FORMAT.format(token), user_id)
    yield user_id, token, generate_authorization_string(None, token)
    features.delete(USER_TOKEN_FORMAT.format(token))


@pytest.fixture
def active_features():
    active = ['feature_3', 'feature_4']
    features.sadd('active_features', *active)
    yield active
    features.delete('active_features')


@pytest.fixture
def features_per_user(user):
    per_user = ['feature_4', 'feature_5']
    features.sadd(USER_FEATURES_FORMAT.format(user[0]), *per_user)
    yield per_user
    features.delete(USER_FEATURES_FORMAT.format(user[0]))


def test_get_features_empty(api_client):
    response = api_client.get('/features')
    assert response.status_code == 200
    assert json.loads(response.data)['active_features'] == []


def test_get_global_features(api_client, global_features):
    response = api_client.get('/features')
    assert response.status_code == 200
    body = json.loads(response.data)
    assert sorted(body['active_features']) == sorted(global_features)


def test_get_auth_error(api_client, user):
    response = api_client.get('/features', headers=dict(Authorization=generate_authorization_string('4', '4')))
    assert response.status_code == 401


def test_get_with_user_global(api_client, user, global_features, features_per_user):
    user_id, token, auth_header = user
    response = api_client.get('/features', headers=dict(Authorization=auth_header))
    assert response.status_code == 200
    body = json.loads(response.data)
    assert sorted(body['active_features']) == sorted(global_features)


def test_get_global_features(api_client, user, global_features, features_per_user, active_features):
    user_id, token, auth_header = user
    response = api_client.get('/features', headers=dict(Authorization=auth_header))
    assert response.status_code == 200
    body = json.loads(response.data)
    assert sorted(body['active_features']) == sorted(global_features + list(set(features_per_user) & set(active_features)))

