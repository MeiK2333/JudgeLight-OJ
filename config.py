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
    webPort = 8000  # WEB 程序使用的端口


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
            'compile': 'python2 -m py_compile main.py',
            'run': 'python2 main.py'
        },
        'python3': {
            'file': 'main.py',
            'compile': 'python3 -m py_compile main.py',
            'run': 'python3 main.py'
        }
    }
    compile_time_limit = 3000  # ms
    compile_memory_limit = 655350  # kb
    default_checker = {
        'file': 'template/checker.py',  # 默认评测程序
        'cmd': 'python3 checker.py'  # 默认评测命令
    }


run_status = {
    '0': {
        'result': 'Accepted',
        'message': 'ok'
    },
    '6': {
        'result': 'Memory Limit Exceeded',
        'message': 'new / malloc error'
    },
    '8':  {
        'result': 'Runtime Error',
        'message': '浮点数例外(除零)'
    },
    '11': {
        'result': 'Memory Limit Exceeded',
        'message': '非法内存操作'
    },
    '14': {
        'result': 'Time Limit Exceeded',
        'message': '程序运行超时'
    },
    '24': {
        'result': 'Time Limit Exceeded',
        'message': '程序运行超时'
    },
    '25': {
        'result': 'Output Limit Exceeded',
        'message': '输出文件过大'
    }
}

checker_status = {
    '0': 'Accepted',
    '256': 'Wrong Answer',
    '512': 'Presentation Error'
}
