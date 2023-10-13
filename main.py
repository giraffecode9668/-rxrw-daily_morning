from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
weather_key = os.environ["WEATHER_KEY"]


def get_weather_work():
  url = "https://restapi.amap.com/v3/weather/weatherInfo?city=440305&extensions=all&key=" + weather_key
  res = requests.get(url).json()
  weather_entity = res['forecasts'][0]
  return weather_entity['city'], weather_entity['casts'][0]['dayweather'], weather_entity['casts'][0]['daytemp_float']

def get_weather_live():
  url = "https://restapi.amap.com/v3/weather/weatherInfo?city=440306&extensions=all&key=" + weather_key
  res = requests.get(url).json()
  weather_entity = res['forecasts'][0]
  return weather_entity['city'], weather_entity['casts'][0]['dayweather'], weather_entity['casts'][0]['daytemp_float']


def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wk_city, wk_dayweather, wk_daytemp_float = get_weather_work()
lv_city, lv_dayweather, lv_daytemp_float = get_weather_live()
data = {"wk_city":{"value":wk_city}, "wk_dayweather":{"value":wk_dayweather}, "wk_daytemp_float":{"value":wk_daytemp_float}, "lv_city":{"value":lv_city}, "lv_dayweather":{"value":lv_dayweather}, "lv_daytemp_float":{"value":lv_daytemp_float}, "words":{"value":get_words(), "color":get_random_color()}}
print(data)
res = wm.send_template(user_id, template_id, data)
print(res)
