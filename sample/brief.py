# -*- coding: utf-8 -*-

import json
import requests
import re
import pandas as pd
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import time

from dateutil import tz
from datetime import datetime

start = time.time()

# UTC Zone
from_zone = tz.gettz('UTC')
# China Zone
to_zone = tz.gettz('Asia/Shanghai')
utc = datetime.utcnow()
# Tell the datetime object that it's in UTC time zone
utc = utc.replace(tzinfo=from_zone)
# Convert time zone
local = utc.astimezone(to_zone)

pd.options.display.max_rows = 200
pd.options.display.max_columns = 200
pd.options.display.width = 1000

all_sh = requests.get('http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.2&sty=FCOIATA&sortType=E&sortRule=-1&page=1&pageSize=2000&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=data&_g=0.19499835146278688')

all_sh_raw_text_tmp = all_sh.text

all_sh_raw_text = re.search(r'var quote_123=\{rank:(.*),pages:.*}',all_sh_raw_text_tmp,re.S)

all_sh_json_text = all_sh_raw_text.group(1)

all_sh_json = json.loads(all_sh_json_text)

records = []

for record in all_sh_json:
    # print record
    records.append(record.split(','))
#
# all_sh_df = pd.DataFrame(records)
all_sh_df = pd.DataFrame(records,columns=['seq', 'code', 'name', 'zuixinjia', 'zhangdiee','zhangdiefu','zhengfu','chengjiaoliang','chengjiaoe','zuoshou','jinkai','zuigao','zuidi','u1','u2','u3','u4','u5','u6','u7','u8','5fengzhong','liangbi','huanshoulv','shiyinglv'])
# print all_sh_df
sh_df_1 = all_sh_df[(all_sh_df['zuixinjia'])!='-']

sh_df_2 = sh_df_1.replace('-', '0')

sh_df_2['zhangdiefu'] = sh_df_2['zhangdiefu'].replace('%','',regex=True).astype('float')

# print sh_df_2

cols_to_convert = ['zuixinjia','zhangdiefu','zhengfu','chengjiaoliang','chengjiaoe','zuoshou','jinkai','zuigao','zuidi','liangbi']

for col in cols_to_convert:
    sh_df_2[col] = sh_df_2[col].astype(float)


#cje
sh_df_2 = sh_df_2.sort_values(['chengjiaoe'],ascending=[0])

sh_df_cje_150 = sh_df_2[:150]

winprob = len(sh_df_cje_150[sh_df_cje_150['zhangdiefu']>0])/150.0
winmedian =  np.median(sh_df_cje_150['zhangdiefu'])

#zxj
sh_df_3 = sh_df_2.sort_values(['zuixinjia'],ascending=[0])

sh_df_zxj_150 = sh_df_3[:150]

winprob_zxj = len(sh_df_zxj_150[sh_df_zxj_150['zhangdiefu']>0])/150.0
winmedian_zxj =  np.median(sh_df_zxj_150['zhangdiefu'])

#sz

all_sz = requests.get('http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._SZAME&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=2000&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.27786655588531173')

all_sz_raw_text_tmp = all_sz.text

all_sz_raw_text = re.search(r'var quote_123=\{rank:(.*),pages:.*}',all_sz_raw_text_tmp,re.S)

all_sz_json_text = all_sz_raw_text.group(1)

all_sz_json = json.loads(all_sz_json_text)

records_sz = []

for record_sz in all_sz_json:
    # print record
    records_sz.append(record_sz.split(','))
#
# all_sh_df = pd.DataFrame(records)
all_sz_df = pd.DataFrame(records_sz,columns=['seq', 'code', 'name', 'zuixinjia', 'zhangdiee','zhangdiefu','zhengfu','chengjiaoliang','chengjiaoe','zuoshou','jinkai','zuigao','zuidi','u1','u2','u3','u4','u5','u6','u7','u8','5fengzhong','liangbi','huanshoulv','shiyinglv'])
# print all_sh_df
sz_df_1 = all_sz_df[(all_sz_df['zuixinjia'])!='-']

sz_df_2 = sz_df_1.replace('-', '0')

sz_df_2['zhangdiefu'] = sz_df_2['zhangdiefu'].replace('%','',regex=True).astype('float')


cols_to_convert = ['zuixinjia','zhangdiefu','zhengfu','chengjiaoliang','chengjiaoe','zuoshou','jinkai','zuigao','zuidi','liangbi']

for col in cols_to_convert:
    sz_df_2[col] = sz_df_2[col].astype(float)


#cje
sz_df_2 = sz_df_2.sort_values(['chengjiaoe'],ascending=[0])

sz_df_cje_150 = sz_df_2[:150]

winprob_sz = len(sz_df_cje_150[sz_df_cje_150['zhangdiefu']>0])/150.0
winmedian_sz =  np.median(sz_df_cje_150['zhangdiefu'])

#zxj
sz_df_3 = sz_df_2.sort_values(['zuixinjia'],ascending=[0])

sz_df_zxj_150 = sz_df_3[:150]

winprob_zxj_sz = len(sz_df_zxj_150[sz_df_zxj_150['zhangdiefu']>0])/150.0
winmedian_zxj_sz =  np.median(sz_df_zxj_150['zhangdiefu'])



ddate = datetime.strftime(local, "%Y-%m-%d %H:%M:%S")
content = "上海 \n成交额前150 prob: %f , \n成交额前150 median : %f, \n高价股前150 prob: %f , \n高价股前150 median : %f \n日期 : %s" % (winprob, winmedian, winprob_zxj, winmedian_zxj,ddate)
content_sz = "\n深证 \n成交额前150 prob: %f , \n成交额前150 median : %f, \n高价股前150 prob: %f , \n高价股前150 median : %f \n日期 : %s" % (winprob_sz, winmedian_sz, winprob_zxj_sz, winmedian_zxj_sz,ddate)
# print msg
#
#
#
#
gmail_user = ""
gmail_password = ""

try:
    msg = MIMEText(content+content_sz)
    msg['Subject'] = "收盘简报"
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, ["2405061829@qq.com"], msg.as_string())
    server.close()

    print 'Email sent!'
except:
    print 'Something went wrong...'




