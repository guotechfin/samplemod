# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import requests
import json
import urllib2


import re

tjson = []

def getPDFUrl(infoCode,rDate):
    from dateutil.parser import parse
    tmp_url = 'http://data.eastmoney.com/report/'+parse(rDate).strftime('%Y'+'%m'+'%d')+'/'+infoCode+'.html'


    html_dcm = urllib2.urlopen(tmp_url).read()
    soup = BeautifulSoup(html_dcm, "lxml")
    try:
        file_url = soup.find_all(text='查看PDF原文')[0].parent.get('href')
        return file_url
    except:
        print('get pdf url failed ' + tmp_url + '\n')
        pass

# pdfurl = getPDFUrl(u'APPH5Ri4N5KVASearchReport',u'2016-09-23T15:54:40')
#
# print pdfurl

for i in range(1,911):
    raw_request = requests.get('http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20KFhOckHz={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p='+str(i)+'&mkt=0&stat=0&cmd=2&code=&rt=49135668')
                               # "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20sfLadxId={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p=3&mkt=0&stat=0&cmd=4&code=&rt=49162654"
    # print raw_request.text
    #
    p = re.compile('var KFhOckHz=(.*)')

    m = p.match(raw_request.text)

    # print m.group(1)

    jobj = json.loads(m.group(1),'utf-8')

    raw_records = jobj[u'data']



    for record in raw_records:

        tjson.append({'author':record[u'author'],'infoCode':record[u'infoCode'],'datetime':record[u'datetime'],'insName':record[u'insName'],'secuName':record[u'secuName'],'secuFullCode':record[u'secuFullCode'],'title':record[u'title'],'pdfurl': getPDFUrl(record[u'infoCode'],record[u'datetime'])})
        print ({'author':record[u'author'],'infoCode':record[u'infoCode'],'datetime':record[u'datetime'],'insName':record[u'insName'],'secuName':record[u'secuName'],'secuFullCode':record[u'secuFullCode'],'title':record[u'title'],'pdfurl': getPDFUrl(record[u'infoCode'],record[u'datetime'])})

# with open('data.json', 'w') as outfile:
#     json.dump(tjson, outfile)

# print json.dumps(tjson)



