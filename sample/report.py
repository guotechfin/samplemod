# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import requests
import json
import urllib2
import time


import re






def getPDFUrl(infoCode):
    #APPH5PaB1P4zASearchReport
    p = re.compile('APP(.*)ASearchReport')
    m = p.match(infoCode)
    key = m.group(1)
    url  = calHashValue(key)
    return "http://pdf.dfcfw.com/pdf/H3_AP{}_1.pdf".format(url)

print getPDFUrl("APPH5PaB1P54ASearchReport")



def scanRange(start,end):
    tjson = []
    for i in range(start,end):
        raw_request = requests.get('http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20KFhOckHz={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=1000&p='+str(i)+'&mkt=0&stat=0&cmd=2&code=&rt=49135668')
        p = re.compile('var KFhOckHz=(.*)')
        m = p.match(raw_request.text)
        jobj = json.loads(m.group(1),'utf-8')
        raw_records = jobj[u'data']

        for record in raw_records:
            tjson.append({"author":record[u"author"],"infoCode":record[u"infoCode"],"datetime":record[u"datetime"],"insName":record[u"insName"],"secuName":record[u"secuName"],"secuFullCode":record[u"secuFullCode"],"title":record[u"title"],"pdfurl": getPDFUrl(record[u"infoCode"])})
            # print ({"author":record[u"author"],"infoCode":record[u"infoCode"],"datetime":record[u"datetime"],"insName":record[u"insName"],"secuName":record[u"secuName"],"secuFullCode":record[u"secuFullCode"],"title":record[u"title"],"pdfurl": getPDFUrl(record[u"infoCode"],record[u"datetime"])})
        time.sleep(2*60)
    return tjson

tmp = scanRange(0,46)

seen = set()

newtmp = []

for d in tmp:
    t = tuple(d.items())
    if t not in seen:
        seen.add(t)
        newtmp.append(t)

with open('all.data', 'w') as outfile:
    for item in newtmp:
        json.dump(item,outfile)
        outfile.write(',\n')







