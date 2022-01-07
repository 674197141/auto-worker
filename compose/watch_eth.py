import requests
from module.timer.task_time import scheduler
from loguru import logger
import json

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

last_price = None


def watch_eth_info():

    url = 'https://api.yitaifang.com/currentPrices/?markets%5B%5D=eth%7Cusdt%7Cbinance'
    res = requests.get(url, headers=header)
    data = res.json()
    logger.info("watch_eth_info:%s" % json.dumps(data))
    price = data["data"]['binance']['eth-usdt']['price']
    global last_price
    if last_price:
        f = (price - last_price) / last_price
        if abs(f) >= 0.05:
            pass
        print(f)
    last_price = price


scheduler.add_job(
    watch_eth_info,
    trigger='interval',
    minutes=10
)
