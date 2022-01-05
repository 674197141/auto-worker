
from configparser import ConfigParser
import os

def local_file(filename):
    dir = os.path.dirname(__file__)
    return os.path.join(dir,filename)

config_dc = {}

class Web:
    port = 8080

class Mail:

    user = ''
    password = ''
    host = ''

    def __init__(self):
        config = ConfigParser()
        config.read(local_file('mail.conf'), encoding='UTF-8')
        mail = config['mail']
        self.user = mail.get('user')
        self.password = mail.get('password')
        self.host = mail.get('host')

def init_config():
    config_dc['mail'] = Mail()
    config_dc['web'] = Web()


def get_config(config_name):
    return config_dc[config_name]


if __name__ == '__main__':
    init_config()
    print(get_config('mail').host)