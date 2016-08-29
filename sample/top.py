# -*- coding: utf-8 -*-

import requests
import csv,json

import pandas as pd

cje0 = requests.get('http://q.10jqka.com.cn/interface/stock/fl/cje/desc/1/hsa/quote')
cje1 = requests.get('http://q.10jqka.com.cn/interface/stock/fl/cje/desc/2/hsa/quote')
cje2 = requests.get('http://q.10jqka.com.cn/interface/stock/fl/cje/desc/3/hsa/quote')

zdf0 = requests.get('http://q.10jqka.com.cn/interface/stock/fl/zdf/desc/1/hsa/quote')
zdf1 = requests.get('http://q.10jqka.com.cn/interface/stock/fl/zdf/desc/2/hsa/quote')
zdf2 = requests.get('http://q.10jqka.com.cn/interface/stock/fl/zdf/desc/3/hsa/quote')

# r.encoding='gbk'

# print (cje0.text.decode('unicode-escape'))

pd.set_option('expand_frame_repr', False)

data_cje0 = cje0.json()[u'data']
data_cje1 = cje1.json()[u'data']
data_cje2 = cje2.json()[u'data']

df_cje0 = pd.DataFrame(data_cje0)
df_cje1 = pd.DataFrame(data_cje1)
df_cje2 = pd.DataFrame(data_cje2)

df_cje = pd.concat([df_cje0,df_cje1,df_cje2],ignore_index=True)


data_zdf0 = zdf0.json()[u'data']
data_zdf1 = zdf1.json()[u'data']
data_zdf2 = zdf2.json()[u'data']

df_zdf0 = pd.DataFrame(data_zdf0)
df_zdf1 = pd.DataFrame(data_zdf1)
df_zdf2 = pd.DataFrame(data_zdf2)

df_zdf = pd.concat([df_zdf0,df_zdf1,df_zdf2],ignore_index=True)

core = pd.merge(df_cje,df_zdf,on=['stockcode'])


print core

