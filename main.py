import time
from config import init_config
from loguru import logger

init_config()
logger.add('./log/runtime_{time}.log', rotation="10 MB")


# from compose.daily_weather import *
from compose.watch_okx import *

from module.timer.task_time import scheduler
scheduler.start()

while 1:
    time.sleep(1)