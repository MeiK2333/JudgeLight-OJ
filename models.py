# coding=utf-8
from config import Config

import json
import redis

rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


def add_judger_to_list(judger):
    rdc.rpush(Config.redisList, judger.run_id)


def get_judge_list():
    l = rdc.llen(Config.redisList)
    judge_list = rdc.lrange(Config.redisList, 0, l)
    judge_list_data = []
    for i in judge_list:
        judge_list_data.append(bytes.decode(i))
    return judge_list_data


class Judger(object):
    def __init__(self, run_id):
        self.run_id = str(run_id)
        self.data = {}  # all data
        self.pid = None
        self.language = None
        self.code = None
        self.result = None
        self.time_limit = None
        self.memory_limit = None
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
            time_limit: int,
            memory_limit: int,
            result: Result,
            data: dict
        }
        """
        data = json.loads(data or '{}')
        self.data = data
        self.pid = data.get('pid')
        self.code = data.get('code')
        self.language = data.get('language')
        self.time_limit = int(data.get('time_limit')) if data.get('time_limit') else None
        self.memory_limit = int(data.get('memory_limit')) if data.get('memory_limit') else None

    def update(self):
        """
        Update data to Redis
        """
        if self.run_id is not None:
            self.data['run_id'] = self.run_id
        if self.pid is not None:
            self.data['pid'] = self.pid
        if self.code is not None:
            self.data['code'] = self.code
        if self.language is not None:
            self.data['language'] = self.language
        if self.time_limit is not None:
            self.data['time_limit'] = self.time_limit
        if self.memory_limit is not None:
            self.data['memory_limit'] = self.memory_limit
        rdc.hset(Config.redisResult, self.run_id, json.dumps(self.data))

    def delete(self):
        if rdc.hget(Config.redisResult, self.run_id):
            rdc.hdel(Config.redisResult, self.run_id)


class Result(object):
    def __init__(self):
        """
        {
            compiler: Runner
            runner: [Runner]
            checker: [Runner]
            result: str
        }
        """
        self.compiler = None
        self.runner = None
        self.checker = None
        self.result = None


class Runner(object):
    def __init__(self):
        """
        {
            state: int
            error: bool
            message: str
        }
        """
        self.state = None
        self.error = None
        self.message = None
