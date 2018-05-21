# coding=utf-8
import json
import logging
import os
import sys

import redis

from config import (ANS_FILE_TEMP, DATA_DIR, DATA_START, IN_FILE_TEMP,
                    LANGUAGES, REDIS_HOST, REDIS_LIST, REDIS_PORT,
                    REDIS_RESULT)


def set_logging():
    _logger = logging.getLogger("Judger")
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    file_handler = logging.FileHandler("judger.log")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)
    # _logger.setLevel(logging.INFO)
    _logger.setLevel(logging.DEBUG)
    return _logger


logger = set_logging()


rdp = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
rdc = redis.StrictRedis(connection_pool=rdp)


def new_solution(pid, runid, code, language, time_limit, memory_limit):
    """ 新建评测任务 """
    judge_data = {
        'pid': str(pid),
        'runid': str(runid),
        'code': str(code),
        'language': str(language),
        'time_limit': int(time_limit),
        'memory_limit': int(memory_limit)
    }
    rdc.rpush(REDIS_LIST, json.dumps(judge_data))

    result_data = {
        "runid": str(runid),
        "pid": str(pid),
        "code": str(code),
        "language": str(language),
        "time_limit": int(time_limit),
        "memory_limit": int(memory_limit),
        "cur": 0,
        "total": 65535,
        "result": "Waiting",
        "tests": []
    }
    rdc.hset(REDIS_RESULT, runid, json.dumps(result_data))


def get_task():
    """ 获取评测任务 """
    task = rdc.blpop(REDIS_LIST)
    data = bytes.decode(task[1])

    try:
        judge_data = json.loads(data)
        pid = str(judge_data['pid'])
        runid = str(judge_data['runid'])
        code = str(judge_data['code'])
        language = str(judge_data['language'])
        time_limit = int(judge_data['time_limit'])
        memory_limit = int(judge_data['memory_limit'])
        solution = Solution(pid=pid, runid=runid, code=code, language=language,
                            time_limit=time_limit, memory_limit=memory_limit)
    except Exception:
        return None

    return solution


def get_result_by_redis(runid):
    """ 由 redis 获得 result """
    data = rdc.hget(REDIS_RESULT, runid)
    return json.loads(data)


class Solution(object):

    def __init__(self, pid, runid, code, language, time_limit, memory_limit):
        self.pid = str(pid)
        self.runid = str(runid)
        self.code = str(code)
        self.language = str(language)
        self.time_limit = int(time_limit)
        self.memory_limit = int(memory_limit)
        self.data = get_dataset(self.pid)

    def judge_json(self):
        judge_json = {}

        judge_json['fifo.out'] = '/judgelight/work/fifo.out'
        judge_json['fifo.err'] = '/judgelight/work/fifo.err'

        judge_json['code'] = self.code
        judge_json['language'] = self.language
        judge_json['time_limit'] = self.time_limit
        judge_json['memory_limit'] = self.memory_limit
        judge_json['data'] = self.data

        judge_json['file_name'] = LANGUAGES[self.language]['file_name']
        judge_json['compile'] = LANGUAGES[self.language]['compile']
        judge_json['run'] = LANGUAGES[self.language]['run']

        validator_data = get_validator(self.pid)
        judge_json['out_validator'] = validator_data['out_validator']
        judge_json['out_validator_common'] = validator_data['out_validator_common']
        return judge_json

    def update(self, cur_data=None, result=None):
        data = {
            "runid": self.runid,
            "pid": self.pid,
            "code": self.code,
            "language": self.language,
            "time_limit": self.time_limit,
            "memory_limit": self.memory_limit,
            "cur": 0,
            "total": len(self.data),
            "result": "",
            "tests": []
        }
        if cur_data is not None:
            data['cur'] = cur_data['cur']
            data['result'] = cur_data['msg']
        if result is not None:
            data.update(get_result(result, self.time_limit, self.memory_limit))
        if data['cur'] > data['total']:
            data['cur'] = data['total']
        rdc.hset(REDIS_RESULT, self.runid, json.dumps(data, indent=4))


def get_result(data, time_limit, memory_limit):
    result = {
        'result': '',
        'tests': []
    }
    result['compile_msg'] = data['compile']['message']

    if data['compile']['exit_code'] != 0 or data['compile']['signal'] != 0:
        result['result'] = 'Compile Error'
        return result

    gr = 'Accepted'
    for run in data['run']:
        r = get_result_str(run, time_limit, memory_limit)
        if r != 'Accepted':
            gr = r
        result['tests'].append({
            "result": r,
            "time_used": run['runner']['time_used'],
            "memory_used": run['runner']['memory_used'],
            "message": run['runner']['message'],
            "exit_code": run['runner']['exit_code'],
            "signal": run['runner']['signal']
        })
    result['result'] = gr
    return result


def get_result_str(run, time_limit, memory_limit):
    if run['runner']['time_used'] > time_limit:
        return 'Time Limit Exceeded'

    if run['runner']['memory_used'] > memory_limit:
        return 'Memory Limit Exceeded'

    if run['runner']['signal'] != 0:
        if run['runner']['signal'] == 14:
            return 'Time Limit Exceeded'
        return 'Runtime Error'

    if run['out_validator']['exit_code'] != 0:
        if run['out_validator']['exit_code'] == 1:
            return 'Wrong Answer'
        if run['out_validator']['exit_code'] == 2:
            return 'Presentation Error'

    if run['out_validator']['signal'] != 0:
        return 'System Error'
    return 'Accepted'


def get_dataset(pid):
    l = os.listdir(os.path.join(DATA_DIR, pid))
    dataset = []
    i = DATA_START
    while True:
        in_temp = IN_FILE_TEMP.format(i)
        ans_temp = ANS_FILE_TEMP.format(i)
        i += 1
        if in_temp in l and ans_temp in l:
            dataset.append({
                'in_file': os.path.join('/judgelight/data', in_temp),
                'ans_file': os.path.join('/judgelight/data', ans_temp)
            })
        else:
            break
    return dataset


def get_validator(pid):
    if not os.path.exists(os.path.join(DATA_DIR, pid, 'validator.json')):
        return {
            'out_validator': None,
            'out_validator_common': None
        }
    with open(os.path.join(DATA_DIR, pid, 'validator.json')) as fr:
        data = fr.read()
    try:
        data = json.loads(data)
    except Exception:
        data = {}
    data = {
        'out_validator': data.get('out_validator'),
        'out_validator_common': data.get('out_validator_common')
    }
    return data


def get_cur_state(string):
    string = string.split('\n')
    cur = {
        'cur': 0,
        'msg': '',
        'string': string
    }
    for i in string:
        if i:
            state = i.split(':')[0]
            if state.startswith('run'):
                cur['cur'] = int(state.split()[1])
                cur['msg'] = 'Running'
            elif state.startswith('out_validator'):
                cur['cur'] = int(state.split()[1]) + 1
                cur['msg'] = 'Running'
            elif state.startswith('init'):
                cur['msg'] = 'Compiling'
            elif state.startswith('compile'):
                cur['cur'] = 1
                cur['msg'] = 'Running'
            cur['string'] = i
    return cur
