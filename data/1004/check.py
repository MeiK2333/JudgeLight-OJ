# coding=utf-8
import os
import sys
from models import Check, AC, WA


def check_one(in_data, out_data, run_data):
    for i in in_data.split():
        if run_data.strip() == i.strip():
            return AC
    return WA


if __name__ == '__main__':
    work_dir = sys.argv[1]
    os.chdir(work_dir)
    check = Check()
    check.check_one = check_one
    check.go()
    check.update()
