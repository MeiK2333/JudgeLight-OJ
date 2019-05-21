import os

CONFIG = {
    'token': os.environ.get('token', 'token')
}

RABBITMQ_DEFAULT_HOST = os.environ.get('RABBITMQ_DEFAULT_HOST', 'localhost')
RABBITMQ_DEFAULT_USER = os.environ.get('RABBITMQ_DEFAULT_USER', 'guest')
RABBITMQ_DEFAULT_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS', 'guest')

CONFIG['celery_broker'] = f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_DEFAULT_HOST}'
CONFIG['celery_backend'] = f'amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_DEFAULT_HOST}'

CONFIG['language'] = {
    'gcc': {
        'filename': 'main.c',
        'compile': '/usr/bin/gcc main.c -o a.out -O2',
        'run': 'a.out',
    },
    'g++': {
        'filename': 'main.cpp',
        'compile': '/usr/bin/g++ main.cpp -o a.out -O2',
        'run': 'a.out',
    },
    'python': {
        'filename': 'main.py',
        'compile': '/bin/echo python',
        'run': '/usr/local/bin/python main.py',
    }
}

CONFIG['data_folder'] = os.environ.get('data_folder', os.path.abspath('data'))
CONFIG['workdir'] = os.environ.get('workdir', os.path.abspath('work'))

if not os.path.exists(CONFIG['workdir']):
    os.mkdir(CONFIG['workdir'])
