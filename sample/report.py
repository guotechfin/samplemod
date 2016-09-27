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



def getPDFUrl(infoCode,rDate):
    from dateutil.parser import parse
    tmp_url = 'http://data.eastmoney.com/report/'+parse(rDate).strftime('%Y'+'%m'+'%d')+'/'+infoCode+'.html'


    html_dcm = urllib2.urlopen(tmp_url).read()
    soup = BeautifulSoup(html_dcm, "lxml")
    try:
        file_url = soup.find_all(text='查看PDF原文')[0].parent.get('href')
        return file_url
    except:
        print('get-pdf-url-failed ' + tmp_url)
        pass

def scanRange(start,end):
    tjson = []
    for i in range(start,end):
        raw_request = requests.get('http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20KFhOckHz={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p='+str(i)+'&mkt=0&stat=0&cmd=2&code=&rt=49135668')
        p = re.compile('var KFhOckHz=(.*)')
        m = p.match(raw_request.text)
        jobj = json.loads(m.group(1),'utf-8')
        raw_records = jobj[u'data']

        for record in raw_records:
            tjson.append({"author":record[u"author"],"infoCode":record[u"infoCode"],"datetime":record[u"datetime"],"insName":record[u"insName"],"secuName":record[u"secuName"],"secuFullCode":record[u"secuFullCode"],"title":record[u"title"],"pdfurl": getPDFUrl(record[u"infoCode"],record[u"datetime"])})
            # print ({"author":record[u"author"],"infoCode":record[u"infoCode"],"datetime":record[u"datetime"],"insName":record[u"insName"],"secuName":record[u"secuName"],"secuFullCode":record[u"secuFullCode"],"title":record[u"title"],"pdfurl": getPDFUrl(record[u"infoCode"],record[u"datetime"])})
    return tjson

#all = []

for k in range(20,910,10):
    print k
    tmp = scanRange(k,k+10)
    #all.extend(tmp)
    #time.sleep(10*60)

    with open('data.out', 'a') as outfile:
        for item in tmp:
            json.dump(item,outfile)
            outfile.write(',\n')
    #all = []
    # json.dump(tjson, outfile)
    time.sleep(10*60)




