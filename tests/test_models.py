# coding=utf-8
from config import Config
from models import Judger, add_judger_to_list

import json
import redis
import unittest

rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


class TestJudger(unittest.TestCase):
    """
    Test Web
    Please run web.py
    don't run manage.py
    """

    test_data = {
        "code": "100",
        "language": "100",
        "memory_limit": "100",
        "pid": "100",
        "run_id": "100",
        "time_limit": "100"
    }

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
        judger.data = {
            "code": "100",
            "language": "100",
            "memory_limit": "100",
            "pid": "1000",
            "run_id": run_id,
            "time_limit": "100"
        }
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
        test_data = {
            "code": "100",
            "language": "100",
            "memory_limit": 100,
            "pid": "100",
            "run_id": "100",
            "time_limit": 100
        }
        run_id = test_data['run_id']
        judger = Judger(run_id)
        judger.data = self.test_data
        judger.update()

        data = rdc.hget(Config.redisResult, run_id)
        data = json.loads(data)

        for i in data:
            self.assertIn(i, test_data.keys())
            self.assertEqual(data[i], test_data[i])

    def test_add_judger_to_list(self):
        test_data = {
            "code": "100",
            "language": "100",
            "memory_limit": "100",
            "pid": "100",
            "run_id": "100",
            "time_limit": "100"
        }
        run_id = test_data['run_id']
        judger = Judger(run_id)
        judger.data = test_data
        judger.update()

        add_judger_to_list(judger)

        tmp = rdc.lpop(Config.redisList)
        self.assertEqual(bytes.decode(tmp), str(run_id))

        for i in range(1000):
            judger = Judger(i)
            data = {
                "code": "100",
                "language": "100",
                "memory_limit": "100",
                "pid": "100",
                "run_id": i,
                "time_limit": "100"
            }
            judger.data = data
            judger.update()
            add_judger_to_list(judger)

        for i in range(1000):
            tmp = rdc.lpop(Config.redisList)
            self.assertEqual(bytes.decode(tmp), str(i))


if __name__ == '__main__':
    unittest.main()
