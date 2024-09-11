import pandas as pd 
import random
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


url_base = 'https://ext.nicovideo.jp/api/getthumbinfo/'
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36",
    # 可以根据需要添加更多的UA字符串
]

info = pd.read_excel('歌曲信息.xlsx')
songs = info['歌名'].to_list()
for week in range(1,80):
    rank = pd.read_excel(f'完整数据/{week}.xlsx')
    for i in rank.index:
        song_title = rank.at[i,'歌名']
        if song_title in songs:
            songs.remove(song_title)
            print(rank.at[i,'歌名'],end=' ')
            info.loc[info['歌名'] == song_title, '封面链接'] = rank.at[i,'封面链接']
            info.loc[info['歌名'] == song_title, '歌曲链接'] = rank.at[i,'歌曲链接']
            song_url = rank.at[i,'歌曲链接']
            if 'sm' in song_url:
                url = url_base + 'sm' + rank.at[i,'歌曲链接'].split('sm')[1]
            elif 'so' in song_url:
                url = url_base + 'so' + rank.at[i,'歌曲链接'].split('so')[1]
            try:
                random_user_agent = random.choice(user_agents)
                headers = {"User-Agent": random_user_agent}
                response = requests.get(url, headers=headers)

                root = ET.fromstring(response.text)
                thumb = root.find('thumb')
                time = thumb.find('first_retrieve').text
                upload_date = datetime.fromisoformat(time).replace(tzinfo=None)
                date_str = upload_date.strftime('%Y.%m.%d')
                print(date_str)
                info.loc[info['歌名'] == song_title, '投稿日期'] = date_str
            except:
                print('出错')

info.to_excel('歌曲信息.xlsx',index=False)


