# coding=utf-8
import json
import redis
import unittest
import requests

from config import Config

rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


class TestWeb(unittest.TestCase):

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

    def test_post(self):
        data = {
            'run_id': '1000',
            'pid': '1000',
            'time_limit': '1000',
            'memory_limit': '65535',
            'language': 'python3',
            'code': 'print("Hello World!")',
            'other': 'other'
        }
        rst = requests.post('http://127.0.0.1:%d/' % Config.webPort, data=data)
        rst = rst.json()

        rdata = rdc.hget(Config.redisResult, data['run_id'])
        rdata = json.loads(rdata)
        for i in rdata:
            self.assertIn(i, rst.keys())
        self.flushall()

    def test_get(self):
        rst = requests.get('http://127.0.0.1:%d/list/' % Config.webPort)
        rst = rst.json()
        self.assertEqual(rst, [])

        data = {
            'run_id': '1000',
            'pid': '1000',
            'time_limit': '1000',
            'memory_limit': '65535',
            'language': 'python3',
            'code': 'print("Hello World!")',
            'other': 'other'
        }
        requests.post('http://127.0.0.1:%d/' % Config.webPort, data=data)

        rst = requests.get('http://127.0.0.1:%d/list/' % Config.webPort)
        rst = rst.json()
        self.assertIn('1000', rst)
        self.flushall()

    def test_delete(self):
        data = {
            'run_id': '1000',
            'pid': '1000',
            'time_limit': '1000',
            'memory_limit': '65535',
            'language': 'python3',
            'code': 'print("Hello World!")',
            'other': 'other'
        }
        requests.post('http://127.0.0.1:%d/' % Config.webPort, data=data)

        requests.delete('http://127.0.0.1:%d/%s/' % (Config.webPort, data['run_id']))
        rst = requests.get('http://127.0.0.1:%d/%s/' % (Config.webPort, data['run_id']))
        rst = rst.json()
        self.assertEqual(rst['code'], None)
        self.assertEqual(rst['language'], None)
        self.assertEqual(rst['memory_limit'], None)
        self.assertEqual(rst['pid'], None)
        self.assertEqual(rst['time_limit'], None)

        self.flushall()


if __name__ == '__main__':
    unittest.main()
