# coding=utf-8
from config import Config

import json
import redis

rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


def add_judger_to_list(judger):
    rdc.rpush(Config.redisList, judger.run_id)


def get_judge_list():
    _l = rdc.llen(Config.redisList)
    judge_list = rdc.lrange(Config.redisList, 0, _l)
    judge_list_data = []
    for i in judge_list:
        judge_list_data.append(bytes.decode(i))
    return judge_list_data


def get_task():
    task = rdc.blpop(Config.redisList)
    run_id = bytes.decode(task[1])
    return run_id


class Judger(object):
    keys = ['run_id', 'pid', 'language', 'code', 'time_limit', 'memory_limit']

    def __init__(self, run_id):
        self.run_id = str(run_id)
        self.pid = None
        self.language = None
        self.code = None
        self.time_limit = None
        self.memory_limit = None
        self.result = None
        self.other = None
        data = rdc.hget(Config.redisResult, run_id)
        if data:
            self.data = json.loads(data)

    @property
    def data(self):
        _data = {
            'run_id': self.run_id,
            'pid': self.pid,
            'language': self.language,
            'code': self.code,
            'time_limit': self.time_limit,
            'memory_limit': self.memory_limit,
        }
        if self.result:
            _data['result'] = self.result.data
        if self.other:
            _data.update(self.other)
        return _data

    @data.setter
    def data(self, data):
        """
        Parse the data in data into a class object
        """
        # Judge that data contains all the required parameters
        assert all(map(self.data.__contains__, self.keys))
        self.pid = data.pop('pid')
        self.language = data.pop('language')
        self.code = data.pop('code')
        self.time_limit = int(data.pop('time_limit'))
        self.memory_limit = int(data.pop('memory_limit'))
        if 'result' in data.keys():
            self.result = Result()
            self.result.data = data.pop('result')
        self.other = data

    def update(self):
        assert all(map(self.data.__contains__, self.keys))
        rdc.hset(Config.redisResult, self.run_id, json.dumps(self.data))

    def delete(self):
        if rdc.hget(Config.redisResult, self.run_id):
            rdc.hdel(Config.redisResult, self.run_id)


class Result(object):
    def __init__(self):
        """
        {
            compiler: Runner
            result: [
                {
                    runner: Runner,
                    checker: Runner
                },
                ...
            ]
        }
        """
        self.compiler = None
        self.result = None

    @property
    def data(self):
        return {
            'compiler': self.compiler.data,
            'result': [{'runner': runner['runner'].data, 'checker': runner['checker'].data} for runner in self.result]
        }

    @data.setter
    def data(self, data):
        self.compiler = Runner()
        self.compiler.data = data['compiler']
        self.result = []
        for i in data['result']:
            runner = Runner()
            checker = Runner()
            runner.data = i['runner']
            checker.data = i['checker']
            self.result.append({
                'runner': runner,
                'checker': checker
            })

    def __str__(self):
        return json.dumps({
            'compiler': self.compiler.data,
            'result': [{'runner': runner['runner'].data, 'checker': runner['checker'].data} for runner in self.result]
        }, ensure_ascii=False, indent=4)


class Runner(object):
    def __init__(self):
        """
        {
            state: int
            message: str
            time_used: int
            memory_used: int
            other: dict
        }
        """
        self.state = None
        self.message = None
        self.time_used = None
        self.memory_used = None
        self.other = None

    @property
    def data(self):
        _data = {
            'state': self.state,
            'message': self.message,
            'time_used': self.time_used,
            'memory_used': self.memory_used,
            'other': self.other
        }
        return _data

    @data.setter
    def data(self, data):
        self.state = data.pop('state')
        self.message = data.pop('message')
        self.time_used = data.pop('time_used')
        self.memory_used = data.pop('memory_used')
        if data:
            self.other = data

    def __str__(self):
        return json.dumps({
            'state': self.state,
            'message': self.message,
            'time_used': self.time_used,
            'memory_used': self.memory_used
        }, ensure_ascii=False, indent=4)
