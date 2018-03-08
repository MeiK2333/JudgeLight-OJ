# coding=utf-8
from config import Config
from models import Judger, add_judger_to_list

import json
import redis
import unittest

rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


class TestJudger(unittest.TestCase):

    def flushall(self):
        keys = rdc.hkeys(Config.redisResult)
        for key in keys:
            rdc.hdel(Config.redisResult, key)
        l = rdc.llen(Config.redisList)
        for i in range(l):
            rdc.lpop(Config.redisList)

    def setUp(self):
        self.flushall()

    def tearDown(self):
        self.flushall()

    def test_judger(self):
        run_id = 1000
        judger = Judger(run_id)
        judger.pid = '1000'
        judger.update()

        judger1 = Judger(run_id)
        self.assertEqual(judger1.pid, '1000')

        judger1.delete()

    def test_delete(self):
        run_id = 1000
        judger = Judger(run_id)
        judger.pid = '1000'
        judger.update()

        judger.delete()

        self.assertEqual(rdc.hget(Config.redisResult, run_id), None)

    def test_update(self):
        run_id = 1000
        judger = Judger(run_id)
        judger.update()

        data = rdc.hget(Config.redisResult, run_id)
        data = json.loads(data)
        self.assertEqual(data, {'run_id': str(run_id)})

        judger.language = 'python3'
        judger.code = 'print("Hello World!")'
        judger.pid = '1000'
        judger.update()

        data = rdc.hget(Config.redisResult, run_id)
        data = json.loads(data)
        self.assertEqual(data,
                         {'run_id': str(run_id), 'language': 'python3', 'code': 'print("Hello World!")', 'pid': '1000'})

    def test_add_judger_to_list(self):
        run_id = 1000
        judger = Judger(run_id)
        judger.update()

        add_judger_to_list(judger)

        tmp = rdc.lpop(Config.redisList)
        self.assertEqual(bytes.decode(tmp), str(run_id))

        for i in range(1000):
            judger = Judger(i)
            judger.update()
            add_judger_to_list(judger)

        for i in range(1000):
            tmp = rdc.lpop(Config.redisList)
            self.assertEqual(bytes.decode(tmp), str(i))


if __name__ == '__main__':
    unittest.main()
