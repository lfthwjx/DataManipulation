__author__ = 'Jun Wang'
# -*- coding:utf-8 -*-
import json,urllib2,sys, MySQLdb
# import pandas as pd
reload(sys)
sys.setdefaultencoding('utf8')
# from pandas import DataFrame,Series

db = MySQLdb.connect(host="localhost",user="root", passwd="wanjun", db="test", use_unicode=True, charset="utf8")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS lagou_it")
db.commit()
cursor.execute('''CREATE TABLE IF NOT EXISTS lagou_it(
                  position_name VARCHAR(100),
                  company_name VARCHAR(100),
                  company_size VARCHAR(100),
                  city VARCHAR(20),
                  industry VARCHAR(200),
                  salary VARCHAR(50),
                  jobnature VARCHAR(20),
                  education VARCHAR(50),
                  workyear VARCHAR(50)
                  )''')
def lagou_spider_keyword():

    i = 0
    # type = 'true'
    url = 'http://www.lagou.com/jobs/positionAjax.json?pn='+str(i+1)
    data = urllib2.urlopen(url).read()
    data_json = json.loads(data)
    # totalCount = int(data_json['content']['positionResult']['totalCount'])
    totalCount = 5000
    resultSize = int(data_json['content']['positionResult']['resultSize'])
    totalPage = totalCount/resultSize+1
    result = []
    for i in range(totalPage):
        # time.sleep(1)
        print 'fetching Page '+str(i)
        url = 'http://www.lagou.com/jobs/positionAjax.json?pn='+str(i+1)
        data = urllib2.urlopen(url).read()
        data_json = json.loads(data)
        resultSize = int(data_json['content']['positionResult']['resultSize'])
        if resultSize>0:
            for j in range(resultSize):
                search_result = data_json['content']['positionResult']['result']
                result_dic = dict(search_result[j])
                companyFullName = result_dic['companyFullName']
                positionName = result_dic['positionName']
                education = result_dic['education']
                city = result_dic['city']
                industryField = result_dic['industryField']
                jobNature = result_dic['jobNature']
                workYear = result_dic['workYear']
                salary = result_dic['salary']
                companySize = result_dic['companySize']
                result_pos = [positionName,companyFullName,companySize,city,industryField,salary,jobNature,education,workYear]
                result.append(result_pos)

    sql = """INSERT INTO lagou_it\
           SET position_name=%s,company_name=%s,company_size=%s,city=%s,industry=%s,salary=%s,jobnature=%s,education=%s,workyear=%s"""
    for x in range(0, len(result)):
        cursor.execute(sql,(result[x][0],result[x][1],result[x][2],result[x][3],result[x][4],result[x][5],result[x][6],result[x][7],result[x][8],))
        db.commit()

if __name__=='__main__':
    # keyword='数据分析' #define search keyword
    lagou_spider_keyword()
