# coding=utf-8

# 各个语言编译和运行的命令
LANGUAGES = {
    'gcc': {
        'file_name': 'main.c',
        'compile': 'gcc main.c -o main.out --std=gnu11 -O2 -Wall',
        'run': './main.out'
    },
    'g++': {
        'file_name': 'main.cpp',
        'compile': 'g++ main.cpp -o main.out --std=gnu++11 -O2 -Wall',
        'run': './main.out'
    },
    'python': {
        'file_name': 'main.py',
        'compile': 'python3 -m py_compile main.py',
        'run': 'python3 main.py'
    },
    'java': {
        'file_name': 'Main.java',
        'compile': 'javac Main.java',
        'run': 'java Main'
    }
}

DATA_DIR = '/home/meik/JudgeLight-OJ/data'  # 数据目录
WORK_DIR = '/home/meik/JudgeLight-OJ/work'  # 工作目录

IN_FILE_TEMP = 'data{}.in'  # 输入数据格式
ANS_FILE_TEMP = 'data{}.out'  # 输出数据格式
DATA_START = 1  # 数据开始组数

UPDATE_TIME = 0.1  # 状态更新的时间间隔

REDIS_HOST = '127.0.0.1'  # redis host
REDIS_PORT = '6379'  # redis port
REDIS_LIST = 'judger:list'  # redis judge list
REDIS_RESULT = 'judger:result'  # redis result hash

JUDGER_COUNT = -1  # 同时评测的最大个数（-1 为默认 CPU 核数）
