# coding=utf-8
from config import Config
from models import Judger

import json
import redis
import unittest

rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


class TestModels(unittest.TestCase):

    def setUp(self):
        keys = rdc.hkeys(Config.redisResult)
        for key in keys:
            rdc.hdel(Config.redisResult, key)

    def test_Judger(self):
        run_id = 1000
        judger = Judger(run_id)
        judger.update()

        data = rdc.hget(Config.redisResult, run_id)
        data = json.loads(data)
        self.assertEqual(data, {})

        judger.language = 'python3'
        judger.code = 'print("Hello World!")'
        judger.pid = '1000'
        judger.update()

        data = rdc.hget(Config.redisResult, run_id)
        data = json.loads(data)
        self.assertEqual(data, {'language': 'python3', 'code': 'print("Hello World!")', 'pid': '1000'})


if __name__ == '__main__':
    unittest.main()
