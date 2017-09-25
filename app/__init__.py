# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging.config
import os

from flask import Flask

from app.config import REDIS_USERS_URL, REDIS_FEATURES_URL
from app.errors import setup_errors
from app.factories import RedisFactory


app = Flask(__name__)
setup_errors(app)

users = RedisFactory.get_instance(REDIS_USERS_URL)
features = RedisFactory.get_instance(REDIS_FEATURES_URL)

logging_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(logging_config, disable_existing_loggers=False)

from app import api

