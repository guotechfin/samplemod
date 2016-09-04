# -*- coding: utf-8 -*-
import requests
import re
import pandas as pd

from core import ashare

pd.options.display.max_rows = 200

dict = ashare()

#sh
cje200sh = requests.get('http://stock.gtimg.cn/data/view/rank.php?t=rankash/turnover&p=1&o=0&l=200&v=list_data')
cje200shlist = re.findall(r"\d{6}",cje200sh.text)
cje200shnames = map(lambda x: dict.get(x),cje200shlist)

cjeshdict = {"code":cje200shlist,"name":cje200shnames}

df1 = pd.DataFrame(data=cjeshdict)

# print df
chr200sh = requests.get('http://stock.gtimg.cn/data/view/rank.php?t=rankash/chr&p=1&o=0&l=200&v=list_data')
chr200shlist = re.findall(r"\d{6}",chr200sh.text)

chrshdict = {"code":chr200shlist}

df2 = pd.DataFrame(data=chrshdict)

rdf = pd.merge(df1,df2,how='inner')

print rdf

#sz
cje200sh = requests.get('http://stock.gtimg.cn/data/view/rank.php?t=rankasz/turnover&p=1&o=0&l=200&v=list_data')
cje200shlist = re.findall(r"\d{6}",cje200sh.text)
cje200shnames = map(lambda x: dict.get(x),cje200shlist)

cjeshdict = {"code":cje200shlist,"name":cje200shnames}

df1 = pd.DataFrame(data=cjeshdict)

# print df
chr200sh = requests.get('http://stock.gtimg.cn/data/view/rank.php?t=rankasz/chr&p=1&o=0&l=200&v=list_data')
chr200shlist = re.findall(r"\d{6}",chr200sh.text)

chrshdict = {"code":chr200shlist}

df2 = pd.DataFrame(data=chrshdict)

rdf = pd.merge(df1,df2,how='inner')

print rdf
