import os

CONFIG = {
    'token': os.environ.get('token', 'token')
}

CONFIG['celery_broker'] = 'amqp://localhost'
CONFIG['celery_backend'] = 'amqp://localhost'

CONFIG['language'] = {
    'gcc': {
        'filename': 'main.c',
        'compile': '/usr/bin/gcc main.c -o a.out -O2',
        'run': 'a.out',
    },
}

CONFIG['data_folder'] = os.path.abspath('data')
CONFIG['workdir'] = os.path.abspath('work')

if not os.path.exists(CONFIG['workdir']):
    os.mkdir(CONFIG['workdir'])
