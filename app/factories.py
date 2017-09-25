# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from redis import StrictRedis


class RedisFactory(object):
    instances = dict()

    @classmethod
    def get_instance(cls, redis_url):
        if redis_url in cls.instances:
            return cls.instances[redis_url]
        instance = StrictRedis.from_url(redis_url)
        cls.instances[redis_url] = instance
        return instance

