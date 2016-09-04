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

def get_data(codelist):
    prefix = lambda x: ("sh" if x.startswith("60") else "sz") + x
    url = "http://qt.gtimg.cn/q=" + ",".join(map(prefix, codelist))

    resp = requests.get(url)

    datas = {}
    for code, line in zip(codelist, resp.text.split("\n")):
        if len(line.strip()) == 0: continue

        m = re.search(r"(.+)=\"(.+)\"", line)
        items = m.group(2).split("~")
        data = float(items[32])
        datas[code] = data

    return datas


# print get_data(chr200shlist)