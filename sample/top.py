import requests
import csv,json


r = requests.get('http://q.10jqka.com.cn/interface/stock/fl/zdf/desc/1/hsa/quote')

data = r.json()[u'data']

print data

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)