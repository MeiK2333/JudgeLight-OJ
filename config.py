# coding=utf-8


class Config(object):
    dataDir = './data/'  # data directory
    workDir = './work/'  # judge work directory
    redisList = 'judge_list'  # redis judge list
    redisResult = 'judge_result'  # redis result hash
    poolCount = -1  # the number of processes（-1 on behalf of the default）
    dockerImage = 'judgelight:latest'  # docker Image
    redisHost = '127.0.0.1'  # redis host
    redisPort = '6379'  # redis port
    webPort = 5000  # web port


class JudgerConfig(object):
    parameter = {
        'gcc': {
            'file': 'main.c',
            'compile': 'gcc main.c -o main.out --std=gnu11 -O2',
            'run': './main.out'
        },
        'g++': {
            'file': 'main.cpp',
            'compile': 'g++ main.cpp -o main.out --std=gnu++11 -O2',
            'run': './main.out'
        },
        'java': {
            'file': 'Main.java',
            'compile': 'javac Main.java',
            'run': 'java Main'
        },
        'python2': {
            'file': 'main.py',
            'compile': 'python2 -m py_compile main.py',
            'run': 'python2 main.py'
        },
        'python3': {
            'file': 'main.py',
            'compile': 'python3 -m py_compile main.py',
            'run': 'python3 main.py'
        }
    }
    compiler_time_limit = 10000  # ms
    compiler_memory_limit = 6553600  # kb
    checker_time_limit = 10000  # ms
    checker_memory_limit = 6553600  # kb
    uid = 100  # set_uid

    _ok = 0  # accepted
    _wa = 1  # wrong answer
    _pe = 2  # presentation error
    _se = 3  # system error
