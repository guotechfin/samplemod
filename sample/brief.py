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

# print records

# print all_sh_json
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

# print ("cje prob: ", winprob)
# print ("cje median: ",winmedian)

#zxj
sh_df_3 = sh_df_2.sort_values(['zuixinjia'],ascending=[0])

sh_df_zxj_150 = sh_df_3[:150]

winprob_zxj = len(sh_df_zxj_150[sh_df_zxj_150['zhangdiefu']>0])/150.0
winmedian_zxj =  np.median(sh_df_zxj_150['zhangdiefu'])

# print ("top price 150 prob: ", winprob_zxj)
# print ("top price 150 median: ",winmedian_zxj)

ddate = datetime.strftime(local, "%Y-%m-%d %H:%M:%S")
content = "成交额前150 prob: %f , \n成交额前150 median : %f, \n高价股前150 prob: %f , \n高价股前150 median : %f \n日期 : %s" % (winprob, winmedian, winprob_zxj, winmedian_zxj,ddate)

# print msg
#
#
#
#
gmail_user = "guo.fintech@gmail.com"
gmail_password = ""

try:
    msg = MIMEText(content)
    msg['Subject'] = "收盘简报"
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, ["2405061829@qq.com"], msg.as_string())
    server.close()

    print 'Email sent!'
except:
    print 'Something went wrong...'




