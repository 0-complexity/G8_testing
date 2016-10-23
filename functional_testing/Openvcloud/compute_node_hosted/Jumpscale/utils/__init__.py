import logging
import os

# Initiate testsuite logger
logger = logging.getLogger('jumpscale_testsuite')
if not os.path.exists('logs/jumpscale_testsuite.log'):
    os.mkdir('logs')
handler = logging.FileHandler('logs/jumpscale_testsuite.log')
formatter = logging.Formatter('%(asctime)s [%(testid)s] [%(levelname)s] %(message)s',
                              '%d-%m-%Y %H:%M:%S %Z')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
