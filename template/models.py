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
        judger = judgelight.JudgeLight()
        judger.time_limit = JudgerConfig.compiler_time_limit
        judger.memory_limit = JudgerConfig.compiler_memory_limit

        fr = open('compiler.out', 'w')
        judger.stderr = fr.fileno()

        judger.fork()
        rst = judger.run(JudgerConfig.parameter[self.language]['compile'])

        fr.close()

        with open('compiler.out') as fr:
            self.compiler = {
                'state': rst.status,
                'message': fr.read()[:1024]
            }
        return True if self.compiler['state'] == 0 else False

    def run_one(self, in_file, out_file):
        pass

    def run(self):
        self.init()
        compile_pass = self.compile_one()
        if compile_pass is False:
            return

        data_list = os.listdir('./data')

        data_cnt = 1
        while True:
            data_in_str = 'data{}.in'.format(data_cnt)
            data_out_str = 'data{}.out'.format(data_cnt)
            if data_in_str in data_list:
                in_file = os.path.join('data', data_in_str)
                out_file = os.path.join('data', data_out_str)
                self.run_one(in_file, out_file)
            else:
                break
            data_cnt += 1
