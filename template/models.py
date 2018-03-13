# coding=utf-8
import json


class JudgeModel(object):

    def __init__(self):
        with open('judge.json') as fr:
            self.judge_data = json.loads(fr.read())

    def init(self):
        pass

    def compile_one(self):
        pass

    def run_one(self):
        pass

    def run(self):
        self.init()
