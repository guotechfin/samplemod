# -*- coding: utf-8 -*-

from datetime import datetime
import pandas as pd
import pandas_datareader.data as web
import numpy as np

pd.set_option('expand_frame_repr', False)


df = pd.read_excel('2016.08.22.vol.157.xlsx')

df = df.groupby(u"所属行业").size().order(ascending=False)

print df
