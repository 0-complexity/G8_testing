import logging
import os
from testconfig import config
from js9 import j

# Initiate testsuite logger
logger = logging.getLogger('testsuite')
if not os.path.exists('logs/testsuite.log'):
    os.mkdir('logs')
handler = logging.FileHandler('logs/testsuite.log')
formatter = logging.Formatter('%(asctime)s [%(testid)s] [%(levelname)s] %(message)s',
                              '%d-%m-%Y %H:%M:%S %Z')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
