# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest

from alembic.command import downgrade, upgrade
from alembic.config import Config


@pytest.fixture(scope='session')
def app():
    from app import app
    return app

@pytest.fixture
def api_client(app):
    test_client = app.test_client()
    return test_client

