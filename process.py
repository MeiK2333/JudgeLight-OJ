# coding=utf-8
from config import Config
from models import Judger

import sys
import logging

# set logging
logger = logging.getLogger("Judger")
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
file_handler = logging.FileHandler("judger.log")
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


def main(judger):
    try:
        logger.info('start judge %s' % judger.run_id)
    except Exception as er:
        logger.error(repr(er))
    else:
        pass
