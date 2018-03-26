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
        self.result = []

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
        judger.uid = JudgerConfig.uid
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
        with open(in_file) as fr:
            input_ = fr.read()
        with open(out_file) as fr:
            output_ = fr.read()
        with open(ans_file) as fr:
            answer = fr.read()

        checker = {
            'message': '标准评测',
            'time_used': -1,
            'memory_used': -1,
        }
        if output_.strip() == answer.strip():
            checker['state'] = JudgerConfig._ok
        elif output_.split() == answer.split():
            checker['state'] = JudgerConfig._pe
        else:
            checker['state'] = JudgerConfig._wa
        return checker

    def run(self):
        self.init()
        compile_pass = self.compile_one()
        if compile_pass is False:
            self.save()
            return

        data_list = os.listdir('./data')

        data_cnt = 1
        judge_all = self.judge_data.get('judge_all', False)  # 是否评测所有数据
        last_judge_state = True  # 上一组数据评测是否正常

        while True:  # 评测所有名称规则为 data{}.in 的数据
            data_in_str = 'data{}.in'.format(data_cnt)
            data_out_str = 'data{}.out'.format(data_cnt)
            data_cnt += 1
            if data_in_str in data_list:
                # 如果参数指定不评测所有数据，那么在遇到评测错误时就会停止评测
                if last_judge_state is False and judge_all is False:
                    break
                in_file = os.path.join('data', data_in_str)
                out_file = os.path.join('data', 'run.out')
                ans_file = os.path.join('data', data_out_str)
                run_rst = self.run_one(in_file, out_file)
                # 如果运行出错，则标记
                if run_rst['state'] != 0:
                    last_judge_state = False
                    # 建立一个空的 checker
                    check_rst = {
                        'message': '',
                        'state': -1,
                        'time_used': -1,
                        'memory_used': -1
                    }
                else:
                    check_rst = self.checker_one(in_file, out_file, ans_file)
                    # 如果答案检查出错，则标记
                    if check_rst['state'] != 0:
                        last_judge_state = False
                self.result.append({
                    'runner': run_rst,
                    'checker': check_rst
                })
            else:
                break
        self.save()

    def save(self):
        judger = {
            'compiler': self.compiler,
            'result': self.result
        }
        with open('result.json', 'w') as fr:  # 结果写入文件
            fr.write(json.dumps(judger))
