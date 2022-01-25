import imp
import requests
from module.timer.task_time import scheduler
from loguru import logger
import json
from config import get_config
import datetime
import base64
import hmac
from hashlib import sha256
import json
from config.okx_api import *
from module.utils import okx_utils
from module.notice.mail import Mail

okx_config = get_config('okx')
base_url = okx_config.get('url')
mail_config = get_config('base')
to_mail = mail_config.get('to_mail')


def get_url(path):
    return base_url+path


def get_header(method, path, body=''):
    time = okx_utils.get_timestamp()
    if not isinstance(body, str):
        body = json.dumps(body)
    base64_data = (time+method+path+body).encode('utf-8')
    acc_sign = okx_config.get('accSign').encode('utf-8')
    sign = base64.b64encode(
        hmac.new(acc_sign, base64_data, digestmod=sha256).digest())
    header = {
        'Content-Type': 'application/json',
        'OK-ACCESS-KEY': okx_config.get('accKey'),
        'OK-ACCESS-SIGN': sign,
        'OK-ACCESS-TIMESTAMP': time,
        'OK-ACCESS-PASSPHRASE': okx_config.get('accPass'),
        'x-simulaed-trading': '0',
    }
    return header


order_dc = {}


def get_order_need_update():
    # 需要更新的订单数据
    path = Api_Trade_Orders_Pending
    url = get_url(path)
    header = get_header('GET', path)
    res = requests.get(url, headers=header)
    data = res.json()
    for order in data['data']:
        if order['instId'] not in order_dc:
            order_dc[order['instId']] = []
        if order['ordId'] not in order_dc[order['instId']]:
            order_dc[order['instId']].append(order['ordId'])


not_state = ['live', 'canceled']


def get_orders():
    # 更新订单数据
    del_list = []
    for instId, orderId in order_dc.items():
        for ordId in orderId:
            path = Api_Trade_Order+"?ordId=" + \
                ordId+'&instId='+instId
            url = get_url(path)
            header = get_header('GET', path)
            res = requests.get(url, headers=header)
            data = res.json()['data'][0]
            log = '合约类型:{instId} 触发价格:{px} 状态:{state}'.format(
                instId=instId, px=data['px'], state=data['state'])
            logger.info(log)
            if data['state'] in not_state:
                continue
            del_list.append([instId, orderId])
            title = '欧易 合约订单触发通知'
            text = '''
                合约类型: {instId}
                触发价格: {px}
            '''.format(instId=instId, px=data['px'])
            mail = Mail.create_mail()
            mail.send(to_mail, title, text)
    for del_ord in del_list:
        order_dc[del_ord[0]].remove(del_ord[1])


def watch_contract_order():
    # 合约订单监控
    logger.info('========运行欧易合约监控========')
    get_order_need_update()
    get_orders()


watch_contract_order()

scheduler.add_job(
	watch_contract_order,
	trigger='interval',
	minutes=2,
)