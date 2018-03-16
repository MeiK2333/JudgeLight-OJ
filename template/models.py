# coding=utf-8
import os
import json
from config import JudgerConfig
import judgelight


class JudgeModel(object):

    def __init__(self):
        with open('judger.json') as fr:
            self.judge_data = json.loads(fr.read())
        self.code = self.judge_data['code']
        self.language = self.judge_data['language']
        self.compiler = None
        self.result = None

    def init(self):
        pass

    def compile_one(self):
        with open(JudgerConfig.parameter[self.language]['file'], 'w') as fr:
            fr.write(self.code)
        compiler = judgelight.JudgeLight()
        compiler.time_limit = JudgerConfig.compiler_time_limit
        compiler.memory_limit = JudgerConfig.compiler_memory_limit

        fr = open('compiler.out', 'w')
        compiler.stderr = fr.fileno()

        compiler.fork()
        rst = compiler.run(JudgerConfig.parameter[self.language]['compile'])

        fr.close()

        with open('compiler.out') as fr:
            self.compiler = {
                'state': rst.status,
                'message': fr.read()[:1024],
                'time_used': rst.time_used,
                'memory_used': rst.memory_used
            }
        return True if self.compiler['state'] == 0 else False

    def run_one(self, in_file, out_file):
        in_file = open(in_file)
        out_file = open(out_file, 'w')
        judger = judgelight.JudgeLight()
        judger.time_limit = self.judge_data['time_limit']
        judger.memory_limit = self.judge_data['memory_limit']
        judger.stdin = in_file.fileno()
        judger.stdout = out_file.fileno()
        judger.fork()

        rst = judger.run(JudgerConfig.parameter[self.language]['run'])

        in_file.close()
        out_file.close()

        runner = {
            'state': rst.status,
            'message': '',
            'time_used': rst.time_used,
            'memory_used': rst.memory_used
        }
        return runner

    def checker_one(self, in_file, out_file, ans_file):
        pass

    def run(self):
        self.init()
        compile_pass = self.compile_one()
        if compile_pass is False:
            return

        data_list = os.listdir('./data')

        self.result = []
        data_cnt = 1
        while True:
            data_in_str = 'data{}.in'.format(data_cnt)
            data_out_str = 'data{}.out'.format(data_cnt)
            if data_in_str in data_list:
                in_file = os.path.join('data', data_in_str)
                out_file = os.path.join('data', 'run.out')
                ans_file = os.path.join('data', data_out_str)
                self.run_one(in_file, out_file)
            else:
                break
            data_cnt += 1
