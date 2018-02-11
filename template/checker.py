# coding=utf-8
import os
import sys

_ok = 0
_wa = 1
_pe = 2
_se = 3


def result(r, msg=''):
    if msg:
        sys.stderr.write(msg)
    sys.exit(r)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        result(_se, 'missing args')
    input_ = sys.argv[1]
    output_ = sys.argv[2]
    answer = sys.argv[3]
    with open(input_) as fr:
        input_ = fr.read()
    with open(output_) as fr:
        output_ = fr.read()
    with open(answer) as fr:
        answer = fr.read()

    if output_.strip() == answer.strip():
        result(_ok)
    if output_.split() == answer.split():
        result(_pe)
    result(_wa)
