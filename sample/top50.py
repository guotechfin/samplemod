# -*- coding: utf-8 -*-
import requests
import re
import pandas as pd

from core import ashare

dict = ashare()

sz50 = requests.get('http://qt.gtimg.cn/r=0.9452569935440971q=aszzdftop50')
sz50s = re.findall(r"\d{6}",sz50.text)
sz50names = map(lambda x: dict.get(x),sz50s)


sh50 = requests.get('http://qt.gtimg.cn/r=0.9452569935440971q=ashzdftop50')
sh50s = re.findall(r"\d{6}",sh50.text)
sh50names = map(lambda x: dict.get(x),sh50s)

d = {'sz': sz50names, 'sh': sh50names}

df = pd.DataFrame(data=d)

print df