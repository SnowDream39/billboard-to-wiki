import requests
import xml.etree.ElementTree as ET
import random
from datetime import datetime, timedelta

url = 'https://ext.nicovideo.jp/api/getthumbinfo/sm42464261'
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36",
    # 可以根据需要添加更多的UA字符串
]
random_user_agent = random.choice(user_agents)
headers = {"User-Agent": random_user_agent}
response = requests.get(url, headers=headers)

root = ET.fromstring(response.text)
thumb = root.find('thumb')
time = thumb.find('first_retrieve').text
upload_date = datetime.fromisoformat(time).replace(tzinfo=None)
print(upload_date.strftime('%Y年%m月%d日'))

begin = datetime(2022,11,30,0,0,0)
week = 30
stat_start = begin + timedelta(days = week*7)
if upload_date - stat_start >= timedelta(0):
    print('NEW!!', week)


