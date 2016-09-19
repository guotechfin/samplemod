# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import json


import re



tjson = []

for i in range(1,321):
    raw_request = requests.get('http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20KFhOckHz={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p='+str(i)+'&mkt=0&stat=0&cmd=2&code=&rt=49135668')

    # print raw_request.text
    #
    p = re.compile('var KFhOckHz=(.*)')

    m = p.match(raw_request.text)

    # print m.group(1)

    jobj = json.loads(m.group(1),'utf-8')

    raw_records = jobj[u'data']



    for record in raw_records:
        tjson.append({'author':record[u'author'],'infoCode':record[u'infoCode'],'datetime':record[u'datetime'],'insName':record[u'insName'],'secuName':record[u'secuName'],'secuFullCode':record[u'secuFullCode'],'title':record[u'title']})
        print ({'author':record[u'author'],'infoCode':record[u'infoCode'],'datetime':record[u'datetime'],'insName':record[u'insName'],'secuName':record[u'secuName'],'secuFullCode':record[u'secuFullCode'],'title':record[u'title']})

with open('data.json', 'w') as outfile:
    json.dump(tjson, outfile)

# print json.dumps(tjson)



