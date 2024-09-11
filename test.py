import pandas as pd

for week in range(1,80):
    week_rank = pd.read_excel(f'完整数据/{week}.xlsx')
    del week_rank['Unnamed: 0']
    week_rank.to_excel(f'完整数据/{week}.xlsx',index=False)