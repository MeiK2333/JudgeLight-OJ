# coding=utf-8
from models import JudgeModel

if __name__ == '__main__':
    judger = JudgeModel()
    judger.run()
    print(judger.judge_data)
