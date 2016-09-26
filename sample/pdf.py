# coding: utf-8
from datetime import datetime #导入日期时间
start_time = datetime.now()

print('+--------------------+') # 日志分隔符无意义

from bs4 import BeautifulSoup
import requests
import urllib
import pandas as pd
import os #文件系统
import shutil #文件复制

# 东方财富通页面地址后缀格式，可用range代替
page_number = 10

# 东方财富通页面地址前缀格式, 感谢http://www.mamicode.com/info-detail-1325623.html
page_url = 'http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HYSR&mkt=0&stat=0&cmd=2&code=&sc=&ps=50&p='

def get_eastmoney_industry_reports(pages):
    # 取回东方财富通行业报告函数
    from bs4 import BeautifulSoup
    import requests
    import urllib
    import pandas as pd
    try: #添加错误处理部分，待完善
        soup2 = []
        for i in range(1, pages+1):
            html_doc = urllib.request.urlopen(page_url + str(i)).read()
            # print('Get the ' + str(i) + 'th Page !')
            soup0 = BeautifulSoup(html_doc, "lxml")
            soup1 = soup0.text[3:][:-3].split('","')
            for j in range(0, len(soup1)): #此处不能用len(soup1)-1,会缺少数据
                soup2.append(soup1[j].replace('&sbquo;', '，').replace('&quot;', '\"').split(','))

        dataf = pd.DataFrame(soup2, columns = ['评级变动', '报告日期', '编号', '机构代码', '机构名称', '机构影响力', '行业代码', '评级类别', '投资评级', '标题', '行业名称', '涨跌幅'])
        dataf.index = dataf['编号']
        dataf.index.name = 'indexs'

        # 去掉标题中的半角引号、半角冒号
        for i in range(0, len(dataf)-1):
            dataf['标题'][i] = dataf['标题'][i].replace(':', '：').replace('"', '')
        # dataf.to_csv('/home/wangshi/script/dfcft_hy')
        # 返回DataFrame
    except:
        print('Fail to get the data!')
    print('Get ' + str(pages) + ' pages!')
    return dataf



def get_eastmoney_report(urls, paths):
    from dateutil.parser import parse
    # 此处待添加验证 urls 是否为 DataFrame
    count_download = 0
    count_pass = 0
    count_fail = 0
    for i in range(0, len(urls)):
        temp_url = 'http://data.eastmoney.com/report/' + parse(urls.loc[urls.index[i]]['报告日期']).strftime('%Y'+'%m'+'%d') + '/hy,' + urls.loc[urls.index[i]]['编号'] + '.html'
        # print(temp_url)
        html_doc = urllib.request.urlopen(temp_url).read()
        soup = BeautifulSoup(html_doc, "lxml")
        try: #增加错误处理部分，可再优化
            file_url = soup.find_all(text = '查看PDF原文')[0].parent.get('href')
            temp_name = paths + parse(urls.loc[urls.index[i]]['报告日期']).strftime('%Y'+'%m'+'%d') + '_' + urls.loc[urls.index[i]]['机构名称'] + '_' + urls.loc[urls.index[i]]['标题'] + '.pdf'

            if os.path.isfile(temp_name) == True:
                # print('File already exist! PASS!')
                count_pass += 1
                pass
            else:
                urllib.request.urlretrieve(file_url, temp_name)
                count_download += 1
                # print('Download ' + str(count_download) + '/' + str(len(urls)) + ' new files '+ 'Successfully !')
        except:
            print('Fail to get the file. ' + 'Please download the file manually !' + '\n'  + temp_url)
            count_fail += 1
            pass

    print('    DOWN: ' + str(count_download) + '/' + str(len(urls)) + '\n'  + '    PASS: ' + str(count_pass) + '/' + str(len(urls)) + '\n'   + '    FAIL: ' + str(count_fail) + '/' + str(len(urls)))

    return

# DataFrame 的差
def df_diff(df_a, df_b):
    df_a_b = df_a.ix[df_a.index.difference(df_b.index)]
    return df_a_b


# DataFrame 的并
def df_all(df_a, df_b):
    df_a_b = df_a.ix[df_a.index.difference(df_b.index)]
    df_all = df_a_b.append(df_b)
    return df_all


# 获取新的数据到 data_temp
data_temp = get_eastmoney_industry_reports(page_number)


print data_temp[:3]


# # 导出新数据 data_new
# data_new = pd.DataFrame(data_temp, columns = ['评级变动', '报告日期', '编号', '机构代码', '机构名称', '机构影响力', '行业代码', '评级类别', '投资评级', '标题', '行业名称', '涨跌幅'])
# data_new.index = data_temp['编号']
# data_new.index.name = 'indexs'
#
#
# # 从文件读取旧数据
# data_old = pd.read_csv('/home/wangshi/reports/script/dfcft_hy', index_col = 'indexs')
#
#
# # 获取新增数据
# data_delta = df_diff(data_new, data_old)
#
#
# # 通过 df_all 函数合并出新的“旧数据”
# data_all = df_all(data_new, data_old)
#
#
# data_medical = df_all(data_delta[data_delta['行业代码'] == '465'], data_delta[data_delta['行业代码'] == '727'])
# get_eastmoney_report(data_medical, '/home/wangshi/reports/medical/')
#
# food_beverage = df_all(data_delta[data_delta['行业代码'] == '438'],data_delta[data_delta['行业代码'] == '477'])
# get_eastmoney_report(food_beverage, '/home/wangshi/reports/food_beverage/')
#
#
# # 将新的文件存盘，并备份为含日期格式的文件
# data_all.to_csv('/home/wangshi/reports/script/dfcft_hy')
# shutil.copyfile('/home/wangshi/reports/script/dfcft_hy', ('/home/wangshi/reports/script/dfcft_hy_' + str((datetime.now()).strftime('%Y%m%d'))))
#
# # 输出处理时间到日志
# end_time = datetime.now()
# print('USED ' + str((end_time - start_time).seconds) + ' seconds!')