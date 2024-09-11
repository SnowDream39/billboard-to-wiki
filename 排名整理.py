import pandas as pd

songs = pd.read_excel('歌曲信息.xlsx')
index = songs['歌名'].values
allrank = pd.DataFrame(index=index, columns = ['入榜次数'])
del songs,index

for week in range(1,81):
    data = pd.read_excel(f'完整数据/{week}.xlsx')
    allrank[week] = None
    for i in data.index:
        song = data.at[i,'歌名']
        allrank.at[song,'入榜次数'] = data.at[i,'入榜次数']
        allrank.at[song,week] = data.at[i,'排名']
    
allrank.to_excel('排名整理.xlsx')
