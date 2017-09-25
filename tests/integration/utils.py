# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64


def generate_authorization_string(username, password):
    return 'Basic ' + base64.b64encode("{}:{}".format(username or '', password or ''))
