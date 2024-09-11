import pandas as pd

info = pd.read_excel('歌曲信息.xlsx')

for week in range(73,74):
    ranking = pd.read_excel(f'完整数据/{week}.xlsx')
    for i in ranking.index:
        if ranking.at[i,'歌名'] not in info['歌名'].values:
            info = info._append({'歌名':ranking.at[i,'歌名'],'初登场':week,'P主':ranking.at[i,'作者']},ignore_index=True)
            print(ranking.at[i,'歌名'])
            

info.to_excel('歌曲信息.xlsx', index=False)
