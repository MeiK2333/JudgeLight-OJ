# coding=utf-8
from config import Config

import json
import redis

rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


class Judger(object):
    def __init__(self, run_id):
        self.run_id = str(run_id)
        self.data = {}  # all data
        self.pid = None
        self.language = None
        self.code = None
        self.result = None
        data = rdc.hget(Config.redisResult, run_id)
        self.parse_data(data)

    def parse_data(self, data):
        """
        Parse strings into Python data
        {
            run_id: str,
            pid: str,
            code: str,
            language: str,
            result: Result,
            data: dict
        }
        """
        data = json.loads(data or '{}')
        self.data = data
        self.pid = data.get('pid')
        self.code = data.get('code')
        self.language = data.get('language')

    def update(self):
        """
        Update data to Redis
        """
        if self.pid:
            self.data['pid'] = self.pid
        if self.code:
            self.data['code'] = self.code
        if self.language:
            self.data['language'] = self.language
        rdc.hset(Config.redisResult, self.run_id, json.dumps(self.data))


class Result(object):
    def __init__(self):
        self.compiler = None
        self.runner = None
        self.checker = None
        self.result = None


class Runner(object):
    def __init__(self):
        pass
