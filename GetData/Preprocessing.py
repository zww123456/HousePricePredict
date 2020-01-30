# -*- encoding=utf-8 -*-
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

data = pd.read_csv('MyData/HouseComplete.csv', index_col=0)
data = data.dropna(axis=0, how='any')

ori_dict = {'南': 'n', '东南': 'dn', '东': 'd', '北': 'b', '南北': 'nb',
            '西北': 'xb', '东北': 'db', '西南': 'xn', '东西': 'dx', '西': 'x'}
trim_dict = {'毛坯': 'No_trim', '简单装修': 'Easy_trim', '精装修': 'Fine_trim', '豪华装修': 'Luxury_trim'}

def adv_dimension(col_dict, col_name):
    all_face = []
    for i in data[col_name]:
        all_face.extend(i.split())
    face = pd.unique(all_face)

    res_df = pd.DataFrame(np.zeros((len(data), len(face))), columns=face)

    for i, index in enumerate(data[col_name]):
        indeces = res_df.columns.get_indexer(index.split())
        res_df.iloc[i, indeces] = 1

    res_df = res_df.rename(columns=col_dict)
    return res_df

ori_df = adv_dimension(ori_dict, 'orientation')
trim_df = adv_dimension(trim_dict,'trim')

def clean_layout(x):
    if '室' in x and '厅' in x and '卫' in x:
        x = x.replace('室', '').replace('厅', '').replace('卫', '').replace(' ', ',')
    return x


def clean_price(x):
    return eval(x.replace(' 元/m²', ''))


def clean_area(x):
    return eval(x.replace('平方米', ''))


def clean_year(x):
    if '年' in x:
        return 2020 - eval(x.replace('年', ''))
    else:
        return 'NULL'


def clean_elevator(x):
    if x == '有':
        return 1
    else:
        return 0


data['layout'] = data['layout'].apply(clean_layout)
data['price'] = data['price'].apply(clean_price)
data['area'] = data['area'].apply(clean_area)
data['year'] = data['year'].apply(clean_year)
data['elevator'] = data['elevator'].apply(clean_elevator)


def get_s(x):
    return eval(x.split(',')[0])


def get_f(x):
    return eval(x.split(',')[1])


def get_t(x):
    return eval(x.split(',')[2])


data['s'] = data['layout'].apply(get_s)
data['f'] = data['layout'].apply(get_f)
data['t'] = data['layout'].apply(get_t)

data = data.join(ori_df)
data = data.join(trim_df)

data = data.drop(['village', 'layout'], axis=1)

# print(list(data.columns))


areaExit_data = data[data['area'] >= 75.0].reset_index(drop=True)
marker_df = areaExit_data[['LATB', 'LNGB', 'price']]
train_data = areaExit_data[['area', 'year', 'No_trim', 'Easy_trim', 'Fine_trim', 'Luxury_trim', 'elevator',
                            'd', 'n', 'x', 'b', 'xb', 'db',
                            'xn', 'dn', 'dx', 'nb', 's', 'f', 't', 'spebuding_num', 'price']]

marker_df.to_csv('MyData/Marker_geo.csv')
train_data.to_csv('MyData/HouseData.csv')
