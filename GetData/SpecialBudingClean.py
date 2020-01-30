# 使用xGeocoding工具得到各站点的地理坐标，再次进行数据处理
import pandas as pd

data = pd.read_csv('MyData/SpecialBudings_geo_ok.csv')

data = data[['Address', 'LATB', 'LNGB']]

data.drop_duplicates(['Address'], keep='first', inplace=True)

data = data.reset_index(drop=True)

data.to_csv('MyData/SpecialBudings_geo.csv')

# =>distance_range.py
