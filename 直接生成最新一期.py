import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import asyncio
from bilibili_api import user, sync, Credential
import json
import random

import xml.etree.ElementTree as ET


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36",
    # 可以根据需要添加更多的UA字符串
]

#获取视频 暂时做不到
'''
uid = 12446725

async def main():
    video_id = await get_latest_video(uid)
    article_id = await get_latest_article(uid)

    binfo = pd.read_excel("视频专栏表.xlsx")
    binfo.at[week,"视频"] = video_id
    binfo.at[week,"专栏"] = article_id
    binfo.to_excel("视频专栏表.xlsx")

    return video_id, article_id
    
# 同步执行入口函数
video_id, article_id = sync(main())
'''

'''
binfo = pd.read_excel("视频专栏表.xlsx")
video_id =  binfo.at[week,"视频"] 
article_id =   int(binfo.at[week,"专栏"]) 
'''
credential = Credential(sessdata="11419cad%2C1729581262%2C9abd9%2A41CjCRHD_U0oxD6Pi4xXeQ_FQxei2Dj00Hh1_7bigSI7c15ai5axryAABKPXnFhhQ79HASVkJwbVhWWHFja2hYdXMycC1ZeFZDUV9Bc2tRTUU3MGxnYjZFTnl2dV9LR3BzbzE3Z3duNUEzZlJRckNuZ2tZMEZxZU9uNGJ6UEt3S1BGVDhielgyOEZ3IIEC",
                        bili_jct="0ba19f7e6cb3210cd46f69a1479c4c3c",
                        buvid3="421282EF-A860-65A1-218B-83A1EC3EA78A31062infoc",
                        dedeuserid="151045420",
                        ac_time_value="83902054ba7cf6fe667a6c9604ae4241")

async def get_latest_video(uid):
    # 实例化用户对象
    u = user.User(uid=uid, credential=credential)
    
    videos = await u.get_videos(order=user.VideoOrder.PUBDATE)
    bvid = videos['list']['vlist'][0]['bvid']

    return bvid

async def get_latest_article(uid):
    # 实例化用户对象
    u = user.User(uid=uid, credential=credential)
    
    articles = await u.get_articles(order=user.ArticleOrder.PUBDATE)
    cvid = articles['articles'][0]['id']

    return cvid

class Billboard:
    def __init__(self, week):
        self.week = week
        self.begin = datetime(2022,11,30)
        if week>=80:
            self.begin += timedelta(days=13*7)
        self.date = self.begin + timedelta(days=week*7 + 5)


    def get_song_datas(self):
        url = "https://www.billboard-japan.com/charts/detail?a=niconico&year=2022&month=12&day=12"


        url = 'https://www.billboard-japan.com/charts/detail?a=niconico' + '&year=' + self.date.strftime("%Y") + '&month=' + self.date.strftime("%m") + '&day=' + self.date.strftime("%d")
        print(url)
        random_user_agent = random.choice(user_agents)
        headers = {"User-Agent": random_user_agent}
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find('tbody')
        song_datas = table.find_all('tr')
        return song_datas

    def get_pubdate(self, id):
        url = 'https://ext.nicovideo.jp/api/getthumbinfo/' + id;
        random_user_agent = random.choice(user_agents)
        headers = {"User-Agent": random_user_agent}
        response = requests.get(url, headers=headers)

        root = ET.fromstring(response.text)
        thumb = root.find('thumb')
        time = thumb.find('first_retrieve').text
        upload_date = datetime.fromisoformat(time).replace(tzinfo=None)
        return upload_date.strftime('%Y.%m.%d')



    def write_song_datas(self):

        song_datas = self.get_song_datas()
        ranking = pd.DataFrame(columns=["排名","变化","上周","封面链接","歌名","歌曲链接","作者", "入榜次数", "投稿日期", "上榜次数", "最高排名"])
        info = pd.read_excel('歌曲信息.xlsx',dtype={"排名":'int64',"最高排名":'int64',"入榜次数":'int64'})
        for data in song_datas:
            rank = data.find(attrs={"headers": 'rank'})
            current = int(rank.find_all('span')[0].text)
            change = rank.find_all('span')[1]['class'][0]
            former = rank.find_all('span')[1].text
            if former:
                former = int(former)


            name = data.find(attrs={"headers": 'name'})
            image = "https://www.billboard-japan.com"+name.find('img')['src']
            if name.find(class_='musuc_title').find('a'):
                song = name.find(class_='musuc_title').find('a').text.strip()
                link = name.find(class_='musuc_title').find('a')['href']
            else:
                song = name.find(class_='musuc_title').text.strip()
                link = ''

            artist = name.find(class_='artist_name')
            if artist.find('a'):
                artist = artist.find('a').text
            else:
                artist = artist.text

            
            check = info[info["歌名"] == song]
            if not check.empty:
                row_index = check.index[0]
                highest = min(current, info.at[row_index, "最高排名"])
                info.at[row_index, "最高排名"] = highest
                pubdate = info.at[row_index, "投稿日期"]
                times = info.at[row_index, "入榜次数"] + 1
                info.at[row_index, "入榜次数"] = times 
            else:
                highest = current
                pubdate = self.get_pubdate(link.split('/')[-1])
                times = int(data.find(attrs={"headers": 'times'}).text)
            print([current,change,former,song,artist,times,image,link])
            ranking = ranking._append({"排名": current, "变化": change, "上周": former, "封面链接": image, "歌名": song, "歌曲链接": link, "作者": artist, "入榜次数": times, "投稿日期": pubdate, "最高排名": highest}, ignore_index=True)

        ranking.to_excel(f'完整数据/{week}.xlsx', index=False)

        for i in ranking.index:
            if ranking.at[i,'歌名'] not in info['歌名'].values:
                info = info._append({'歌名':ranking.at[i,'歌名'],'初登场':week,'P主':ranking.at[i,'作者'], "封面链接": ranking.at[i,'封面链接'],"投稿日期": ranking.at[i,'投稿日期'], "歌曲链接": ranking.at[i,'歌曲链接'], "最高排名": ranking.at[i,'最高排名']},ignore_index=True)
                print(ranking.at[i,'歌名'])
        info.to_excel('歌曲信息.xlsx', index=False)

        input("现在请您去填写歌曲信息。")

    def judge_new(self, pubdate):
        start_time = self.date - timedelta(days=14)
        pubdate = datetime.strptime(pubdate, "%Y.%m.%d")
        return 'new' if pubdate >= start_time else 'up'

    def write_entry(self):
        info = pd.read_excel('歌曲信息.xlsx')

        ranking = pd.read_excel(f'完整数据/{week}.xlsx')
        text = open(f'新版条目/{week}.txt', 'w',encoding='UTF-8')


        release = self.begin + timedelta(days = week*7)

        text.write('{{Billboard|index='+str(week)+
                '}}\n\n'
                "'''Billboard JAPAN'''在"
                +release.strftime("%Y年%m月%d日")+
                f"发布了'''NICONICO VOCALOID SONGS TOP20 第{week}期'''。\n\n")



        text.write('==榜单==\n')

        for i in ranking.index:
            data = ranking.loc[i]
            current = data['排名']
            former = '' if pd.isna(data['上周']) else int(data['上周'])
            times =  data['入榜次数']
            name = data['歌名']
            artist = data['作者']
            highest = data['最高排名']
            date = info[info['歌名'] == ranking.at[i,'歌名']].iloc[0]['投稿日期']
            change = self.judge_new(date) if data['变化'] == 'new' else data['变化']
            try:
                link = data['歌曲链接'].split('/')[-1]
            except:
                print(f'第{week}期没有链接')
                break
                
            image = data['封面链接']
            
            if name in info['歌名'].values:
                song_info = info.loc[info['歌名'] == name, ['歌姬', '条目','P主条目','自定义P主']]
                singer = song_info['歌姬'].values[0] if not song_info['歌姬'].isnull().values.any() else ''
                entry = song_info['条目'].values[0] if not song_info['条目'].isnull().values.any() else ''
                artist_entry = song_info['P主条目'].values[0] if not song_info['P主条目'].isnull().values.any() else ''
                artist_diy = song_info['自定义P主'].values[0] if not song_info['自定义P主'].isnull().values.any() else ''       
                
            text.write('{{Billboard/bricks\n'
                    f'|本周 = {current}\n'
                    f'|变化 = {change}\n'
                    f'|上周 = {former}\n'
                    f'|入榜次数 = {times}\n'
                    f'|最高名次 = {highest}\n'
                    f'|曲名 = {name}\n')
            if entry:
                text.write(f'|条目 = {entry}\n')
            text.write(f'|歌姬 = {singer}\n'
                    f'|P主 = {artist}\n')
            if artist_entry:
                text.write(f'|P主条目 = {artist_entry}\n')
            if artist_diy:
                text.write(f'|自定义P主 = {artist_diy}\n')
            
            text.write(f'|id = {link}\n'
                    f'|图片 = {image}\n'
                    f'|投稿日期 = {date}\n'
                    '}}\n\n')

        text.write('== 杂谈 ==\n\n'
                   '== 外部链接 ==\n\n'
                   '[[分类:NICONICO VOCALOID SONGS TOP20]]')
        text.close()

    def main(self):
        self.write_song_datas()
        self.write_entry()

if __name__ == "__main__":

    week = int(input('期数：'))
    billboard = Billboard(week)
    billboard.main()
    