from math import sin,cos,asin,sqrt,radians
import pandas as pd
# 根据地理坐标计算出两地距离
def geodistance(lat1,lng1,lat2,lng2):

    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)]) # 经纬度转换成弧度
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distan =2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
    distan =round(distan/1000,3)
    return distan

sb_geo = pd.read_csv('MyData/SpecialBudings_geo.csv',index_col=0)

house_data = pd.read_csv('MyData/House.csv',names=['village', 'layout', 'price', 'area', 'year',
                                                   'orientation', 'floor', 'trim', 'elevator','LATB','LNGB'])


spebuding_num = []
for i in range(len(house_data)):
    count = 0
    for j in range(len(sb_geo)):
        if geodistance(house_data.iloc[i]['LATB'],house_data.iloc[i]['LNGB'],
                       sb_geo.iloc[j]['LATB'],sb_geo.iloc[j]['LNGB']) <= 2.0:
            count += 1
    spebuding_num.append(count)


house_data['spebuding_num'] = spebuding_num

house_data.to_csv('MyData/HouseComplete.csv')

# =>Preprocessing.py

