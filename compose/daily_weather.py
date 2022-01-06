from config import get_config
import requests
from module.timer.task_time import scheduler
from module.notice.mail import Mail


def get_weather():
    config = get_config('weather')
    city = config.get('city')
    prov = config.get('province')
    url = "https://wis.qq.com/weather/common?source=pc&weather_type=observe|forecast_24h|air&province={prov}&city={city}".format(
        prov=prov, city=city)
    res = requests.get(url)
    res.encoding = 'utf-8'
    print(res.json())
    return city, res.json()["data"]


def daily_weather():
    city, data = get_weather()
    observe = data["observe"]
    title = '天气定时任务'
    text = '''
        当前天气城市: {city}
        天气情况: {weather}
        温度: {degree}
    '''.format(city=city, weather=observe["weather"], degree=observe["degree"])
    config = get_config('base')
    to_mail = config.get('to_mail')
    mail = Mail.create_mail()
    mail.send(to_mail, title, text)


scheduler.add_job(daily_weather, trigger='cron',
                  hour=8)

daily_weather()
