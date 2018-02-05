# coding=utf-8
import os
import json
import judgelight


class Run(object):

    def __init__(self):
        self.run_data = {
            'compile': {
                'pass': True,
                'msg': ''
            },
            'run': [],
            'time_limit': -1,
            'memory_limit': -1
        }
        with open('judge.json') as f:
            self.json_data = json.loads(f.read())

        self.run_init = None
        self.run_one = None

        self.time_limit = self.json_data['time_limit']
        self.memory_limit = self.json_data['memory_limit']
        self.run_cmd = self.json_data['run_cmd']

    def go(self):
        if self.run_init:
            self.run_init()

        self.run_data['compile']['pass'] = self.compile_it()
        with open('compile.out') as f:
            self.run_data['compile']['msg'] = f.read()
        if self.run_data['compile']['pass'] is False:
            return

        if self.run_one is None:
            self.run_one = self.run_one_default

        self.run_data['time_limit'] = self.json_data['time_limit']
        self.run_data['memory_limit'] = self.json_data['memory_limit']
        for i in range(len(self.json_data['data'])):
            rst = self.run_one(os.path.join('data', self.json_data['data'][i]["in"]),
                               os.path.join('data', self.json_data['data'][i]["run"]))
            self.run_data['run'].append({
                'time_used': rst.time_used,
                'memory_used': rst.memory_used,
                'error': rst.error
            })
            if rst.error != 0:
                return

    def compile_it(self):
        compile_cmd = self.json_data['compile_cmd']
        compile_time_limit = self.json_data['compile_time_limit']
        compile_memory_limit = self.json_data['compile_memory_limit']

        compile_judge = judgelight.JudgeLight()
        compile_judge.time_limit = compile_time_limit
        compile_judge.memory_limit = compile_memory_limit

        compile_out_file = open('compile.out', 'w')
        compile_judge.stderr = compile_out_file.fileno()

        compile_judge.fork()
        rst = compile_judge.run(compile_cmd)

        compile_out_file.close()

        if rst.status == 0:
            return True
        return False

    def update(self):
        with open('run_out.json', 'w') as f:
            f.write(json.dumps(self.run_data))

    def run_one_default(self, in_file, out_file):
        run_judge = judgelight.JudgeLight()
        run_judge.time_limit = self.time_limit
        run_judge.memory_limit = self.memory_limit

        in_file = open(in_file)
        run_judge.stdin = in_file.fileno()
        out_file = open(out_file, 'w')
        run_judge.stdout = out_file.fileno()

        run_judge.fork()
        rst = run_judge.run(self.run_cmd)

        return rst


class Check(object):

    def __init__(self):
        self.result_data = {
            'result': '',
            'compile': {
                'pass': True,
                'msg': ''
            },
            'run': [],
            'check': []
        }

        with open('judge.json') as f:
            self.judge_json = json.loads(f.read())

        with open('run_out.json') as f:
            self.run_json = json.loads(f.read())

        self.check_one = None

        self.time_limit = self.run_json['time_limit']
        self.memory_limit = self.run_json['memory_limit']

    def go(self):
        if self.check_one is None:
            self.check_one = self.check_one_default

        self.result_data['compile'] = self.run_json['compile']
        if self.result_data['compile']['pass'] is False:
            self.result_data['result'] = 'Compile Error'
            return

        self.result_data['run'] = self.run_json['run']
        if self.all_run_pass() is False:
            self.result_data['result'] = self.get_run_error()
            return

        for i in range(len(self.judge_json['data'])):
            with open(os.path.join('data', self.judge_json['data'][i]['in'])) as f:
                in_data = f.read()
            with open(os.path.join('data', self.judge_json['data'][i]['out'])) as f:
                out_data = f.read()
            with open(os.path.join('data', self.judge_json['data'][i]['run'])) as f:
                run_data = f.read()
            rst = self.check_one(in_data, out_data, run_data)
            self.result_data['check'].append(rst)
            if rst != 'Accepted':
                self.result_data['result'] = rst
                return False
        self.result_data['result'] = 'Accepted'
        return True

    def update(self):
        with open('judge_out.json', 'w') as f:
            f.write(json.dumps(self.result_data))

    def all_run_pass(self):
        for i in self.run_json['run']:
            if i['error'] != 0:
                return False
        return True

    def get_run_error(self):
        time_limit = self.run_json['time_limit']
        memory_limit = self.run_json['memory_limit']
        for i in self.run_json['run']:
            if i['error'] == 0:
                continue
            if i['time_used'] > time_limit:
                return 'Time Limit Exceeded'
            elif i['memory_used'] > memory_limit:
                return 'Memory Limit Exceeded'
            else:
                return 'Runtime Error'

    def check_one_default(self, in_data, out_data, run_data):
        if out_data.rstrip() == run_data.rstrip():  # 忽略末尾空白符
            return 'Accepted'
        if out_data.split() == run_data.split():  # 如果除了空白符之外全相同
            return 'Presentation Error'
        return 'Wrong Answer'


AC = 'Accepted'
WA = 'Wrong Answer'
PE = 'Presentation Error'
RE = 'Runtime Error'
TLE = 'Time Limit Exceeded'
MLE = 'Memory Limit Exceeded'
