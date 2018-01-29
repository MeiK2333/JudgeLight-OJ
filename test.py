# coding=utf-8
import time
import requests

if __name__ == '__main__':
    for i in range(100):
        requests.post('http://127.0.0.1:8000/', {'run_id': str(i), 'code': '123', 'pid': '123'})
        time.sleep(0.5)
