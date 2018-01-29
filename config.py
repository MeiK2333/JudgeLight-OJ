# coding=utf-8


class Config(object):
    workDir = './work/'  # judge 工作目录
    redisList = 'judge_list'  # Redis 评测队列名
    redisResult = 'judge_result'  # Redis 评测结果哈希名
    redisHost = '127.0.0.1'  # Redis host
    redisPort = '6379'  # Redis port
    poolCount = -1  # 评测进程个数（-1 为默认）
