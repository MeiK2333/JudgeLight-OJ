# coding=utf-8
import os
import json
import judgelight


class Run(object):

    def __init__(self):
        self.run_data = {
            'compile': {
                'pass': True,
                'message': ''
            },
            'run': []
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
        self.run_data['compile']['time_used'] = self.compile_time_used
        self.run_data['compile']['memory_used'] = self.compile_memory_used
        self.run_data['compile']['status'] = self.compile_status
        with open('compile.out') as f:  # 读取编译时的输出
            self.run_data['compile']['message'] = f.read()[:1000]
        if self.run_data['compile']['pass'] is False:
            return

        if self.run_one is None:
            self.run_one = self.run_one_default

        for i in range(len(self.json_data['data'])):
            rst = self.run_one(os.path.join('data', self.json_data['data'][i]["in"]),
                               os.path.join('data', self.json_data['data'][i]["run"]))
            self.run_data['run'].append({
                'time_used': rst.time_used,
                'memory_used': rst.memory_used,
                'pass': True if rst.error == 0 else False,
                'status': rst.status
            })

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

        self.compile_time_used = rst.time_used
        self.compile_memory_used = rst.memory_used
        self.compile_status = rst.status

        return True if rst.status == 0 else False

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
