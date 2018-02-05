# coding=utf-8
import os
import sys
from models import Check

if __name__ == '__main__':
    if len(sys.argv) > 1:
        work_dir = sys.argv[1]
        os.chdir(work_dir)
    check = Check()
    check.go()
    check.update()
