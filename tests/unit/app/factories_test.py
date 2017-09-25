# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest

from mock import Mock

from app.factories import RedisFactory


@pytest.fixture
def strict_redis(mocker):
    return mocker.patch('app.factories.StrictRedis')


class TestRedisFactory(object):
    @staticmethod
    def test_get_instance_fresh(strict_redis):
        url = 'url'
        r = RedisFactory.get_instance(url)
        assert r == strict_redis.from_url.return_value
        strict_redis.from_url.assert_called_with(url)
        assert url in RedisFactory.instances
        assert RedisFactory.instances[url] == r

    @staticmethod
    def test_get_instance_cached(strict_redis):
        url = 'url'
        instance = Mock()
        RedisFactory.instances[url] = instance
        r = RedisFactory.get_instance(url)
        assert r == instance
        assert not strict_redis.from_url.called
        assert url in RedisFactory.instances
        assert RedisFactory.instances[url] == r

