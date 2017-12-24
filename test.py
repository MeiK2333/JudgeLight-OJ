# coding=utf-8
import os
import json
import shutil

def load_json_file(path):
    jfile = open(path)
    jdata = json.loads(jfile.read())
    jfile.close()
    return jdata

def test(pid, runid):
    if os.path.exists(os.path.join('work', runid)):
        shutil.rmtree(os.path.join('work', runid))

    data_json = load_json_file(os.path.join('data', pid, 'data.json'))
    os.mkdir(os.path.join('work', runid))

    shutil.copyfile(os.path.join('data', pid, 'data.json'), os.path.join('work', runid, 'data.json'))
    if data_json['judge_type'] == 'standard':
        shutil.copyfile(os.path.join('judge', 'standard', 'config.py'), os.path.join('work', runid, 'config.py'))
        shutil.copyfile(os.path.join('judge', 'standard', 'judge.py'), os.path.join('work', runid, 'judge.py'))

if __name__ == '__main__':
    test('1000', '1000')
