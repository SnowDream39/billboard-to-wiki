import pandas as pd
from datetime import datetime, timedelta


begin = datetime(2022,11,30)

info = pd.read_excel('歌曲信息.xlsx')
binfo = pd.read_excel('视频专栏表.xlsx')

for week in range(101,103):
    print(week)
    ranking = pd.read_excel(f'完整数据/{week}.xlsx')
    text = open(f'输出条目/{week}.txt', 'w',encoding='UTF-8')

    release = begin + timedelta(days = week*7)

    text.write('{{Billboard|index='+str(week)+
               '}}\n\n'
               "'''Billboard JAPAN'''在"
               +release.strftime("%Y年%m月%d日")+
               f"发布了'''NICONICO VOCALOID SONGS TOP20 第{week}期'''。\n\n")

    

    text.write('==榜单==\n')

    for i in ranking.index:
        data = ranking.loc[i]
        current = data['排名']
        name = data['歌名']
        artist = data['作者']
        try:
            link = data['歌曲链接'].split('/')[-1]
        except:
            print(f'第{week}期没有链接')
            break
            
        image = data['封面链接']
        
        singer = ''
        entry = ''
        artist_entry = ''
        artist_diy = ''
        if name in info['歌名'].values:
            song_info = info.loc[info['歌名'] == name, ['歌姬', '条目','P主条目','自定义P主']]
            singer = song_info['歌姬'].values[0] if not song_info['歌姬'].isnull().values.any() else ''
            entry = song_info['条目'].values[0] if not song_info['条目'].isnull().values.any() else ''
            artist_entry = song_info['P主条目'].values[0] if not song_info['P主条目'].isnull().values.any() else ''
            artist_diy = song_info['自定义P主'].values[0] if not song_info['自定义P主'].isnull().values.any() else ''       
            
        text.write('{{Billboard/bricks\n'
                   f'|本周 = {current}\n'
                   f'|上周 = \n'
                   f'|曲名 = {name}\n'
                   f'|条目 = {entry}\n'
                   f'|歌姬 = {singer}\n'
                   f'|P主 = {artist}\n')
        if artist_entry:
            text.write(f'|P主条目 = {artist_entry}\n')
        if artist_diy:
            text.write(f'|自定义P主 = {artist_diy}\n')
        
        text.write(f'|id = {link}\n'
                   f'|图片 = {image}\n'
                   '}}\n')


    text.write('==杂谈==\n'
               '（待补充）\n\n'
               '{{NICONICO VOCALOID SONGS TOP20}}\n\n'
               '==外部链接==\n')

    if week >= 16:
        video = binfo.at[week,'视频']
        text.write('{{BilibiliVideo|id='+str(video)+
                   '}}\n')

    column = int(binfo.at[week,'专栏'])
    text.write(f'*[https://www.bilibili.com/read/cv{column}'
               ' 文字专栏版]\n\n')

    text.write('[[分类:NICONICO VOCALOID SONGS TOP20]]')

    text.close()
