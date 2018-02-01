# coding=utf-8


class Config(object):
    dataDir = './data/'  # 数据目录
    workDir = './work/'  # judge 工作目录
    redisList = 'judge_list'  # Redis 评测队列名
    redisResult = 'judge_result'  # Redis 评测结果哈希名
    redisHost = '127.0.0.1'  # Redis host
    redisPort = '6379'  # Redis port
    poolCount = -1  # 评测进程个数（-1 为默认）
    dockerImage = 'judgelight:latest'  # 使用的 docker 镜像


class Judge(object):
    cmd = {
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
            'compile': 'ls',
            'run': 'python2 main.py'
        },
        'python3': {
            'file': 'main.py',
            'compile': 'ls',
            'run': 'python3 main.py'
        }
    }
    compile_time_limit = 3000  # ms
    compile_memory_limit = 655350  # kb
