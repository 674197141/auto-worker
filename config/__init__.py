
from configparser import ConfigParser
import os

def local_file(filename):
    dir = os.path.dirname(__file__)
    return os.path.join(dir,filename)

config_dc = {}

class Web:
    port = 8080


def init_config():
    config_dc['web'] = Web()
    config = ConfigParser()
    config.read(local_file('config.conf'), encoding='UTF-8')
    config_dc['base'] = config['base']
    config_dc['weather'] = config['weather']
    config_dc['mail'] = config['mail']


def get_config(config_name):
    return config_dc[config_name]


if __name__ == '__main__':
    init_config()
    print(get_config('mail').host)