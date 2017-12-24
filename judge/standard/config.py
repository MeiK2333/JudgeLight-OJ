# coding=utf-8

compile_time_limit = 5000  # ms 编译时间限制
compile_memory_limit = 655350  # kb 编译内存限制

judge_cmd = {
    "gcc": {
        "code_file": "main.c",  # 代码保存的文件名
        "compile_cmd": "gcc main.c -o main.out",  # 编译参数
        "run_cmd": "./main.out"  # 运行参数
    },
    "g++": {
        "code_file": "main.cpp",
        "compile_cmd": "g++ main.cpp -o main.out --std=gnu++11",
        "run_cmd": "./main.out"
    },
    "python2": {
        "code_file": "main.py",
        "compile_cmd": "ls",
        "run_cmd": "python main.py"
    },
    "python3": {
        "code_file": "main.py",
        "compile_cmd": "ls",
        "run_cmd": "python3 main.py"
    }
}
