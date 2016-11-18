__author__ = 'Jun Wang'
# -*- coding:utf-8 -*-
import MySQLdb, sys
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf8')
db = MySQLdb.connect(host="localhost",user="root", passwd="wanjun", db="test", use_unicode=True, charset="utf8")
# cursor = db.cursor()
sql_sh = 'SELECT * FROM lagou_data_analysis WHERE city="上海"'
sql_bj = 'SELECT * FROM lagou_data_analysis WHERE city="北京"'
sql_gz = 'SELECT * FROM lagou_data_analysis WHERE city="广州"'
sql_ug = 'SELECT * FROM lagou_data_analysis WHERE education="本科"'
sql_dz = 'SELECT * FROM lagou_data_analysis WHERE education="大专"'
sql_ms = 'SELECT * FROM lagou_data_analysis WHERE education="硕士"'
sql_ph = 'SELECT * FROM lagou_data_analysis WHERE education="博士"'
sql_da = 'SELECT * FROM lagou_data_analysis'
sql_it = 'SELECT * FROM lagou_it'

# sql_sh_zl = 'SELECT * FROM zhaopin_data_mining WHERE city="上海"'
# sql_bj_zl = 'SELECT * FROM zhaopin_data_mining WHERE city="北京"'
# sql_gz_zl = 'SELECT * FROM zhaopin_data_mining WHERE city="广州"'
sql_it_zl = 'SELECT * FROM zhaopin_it'
sql_dm_zl = 'SELECT * FROM zhaopin_data_mining'
# sh = cursor.fetchall()
df_it = pd.read_sql(sql_it, db)
df_sh = pd.read_sql(sql_sh, db)
df_bj = pd.read_sql(sql_bj, db)
df_gz = pd.read_sql(sql_gz, db)
df_da = pd.read_sql(sql_da, db)
df_ug = pd.read_sql(sql_ug, db)
df_ms = pd.read_sql(sql_ms, db)
df_dz = pd.read_sql(sql_dz, db)
df_ph = pd.read_sql(sql_ph, db)
df_ug = df_ug.append(df_dz)

# df_sh_zl = pd.read_sql(sql_sh_zl,db)
# df_bj_zl = pd.read_sql(sql_bj_zl,db)
# df_gz_zl = pd.read_sql(sql_gz_zl,db)

df_it_zl = pd.read_sql(sql_it_zl,db)
df_dm_zl = pd.read_sql(sql_dm_zl,db)
sh_city = str('上海').decode('utf-8')
df_sh_zl = df_dm_zl[df_dm_zl['city'].str.contains(sh_city)]
bj_city = str('北京').decode('utf-8')
df_bj_zl = df_dm_zl[df_dm_zl['city'].str.contains(bj_city)]
gz_city = str('广州').decode('utf-8')
df_gz_zl = df_dm_zl[df_dm_zl['city'].str.contains(gz_city)]
ug_edu = str('本科').decode('utf_8')
dz_edu = str('大专').decode('utf_8')
ms_edu = str('硕士').decode('utf_8')
ph_edu = str('博士').decode('utf_8')
df_ug_zl = df_dm_zl[df_dm_zl['education'].str.contains(ug_edu)]
df_dz_zl = df_dm_zl[df_dm_zl['education'].str.contains(dz_edu)]
df_ms_zl = df_dm_zl[df_dm_zl['education'].str.contains(ms_edu)]
df_ph_zl = df_dm_zl[df_dm_zl['education'].str.contains(ph_edu)]
df_ug_zl = df_ug_zl.append(df_dz_zl)

edu = [[len(df_ug),len(df_ms),len(df_ph)],[len(df_ug_zl),len(df_ms_zl),len(df_ph_zl)]]

num_pos_dm = [len(df_da),len(df_dm_zl)]
num_pos_dm_sh = [len(df_sh),len(df_sh_zl)]
num_pos_dm_bj = [len(df_bj),len(df_bj_zl)]
num_pos_dm_gz = [len(df_gz),len(df_gz_zl)]

keywords_data = str('数据').decode('utf-8')
lagou_data = df_it[df_it['position_name'].str.contains(keywords_data)]
zhaopin_data = df_it_zl[df_it_zl['position_name'].str.contains(keywords_data)|df_it_zl['job_description'].str.contains(keywords_dm)]
num_pos_it = [len(df_it),len(df_it_zl)]
num_pos_datainit = [len(lagou_data),len(zhaopin_data)]

def lagou_split(df_da):
    split = lambda x: pd.Series(x.split('-'))
    df_salary_lagou = df_da['salary'].apply(split)
    df_salary_lagou = df_salary_lagou.rename(columns={0: 'Min Salary', 1: 'Max Salary'})
    return df_salary_lagou

def zhaopin_split_min(df_dm_zl):
    split = lambda x: pd.Series(x.split('-'))
    df_salary_zhaopin = df_dm_zl['salary'].apply(split)
    df_salary_zhaopin = df_salary_zhaopin.rename(columns={0:'Min Salary',1:'Max Salary'}).dropna()
    int_x = lambda x:pd.Series(str(int(x)/1000)+'k')
    df_min = df_salary_zhaopin['Min Salary'].apply(int_x)
    df_min = df_min.rename(columns={0:'Min Salary'})
    # df_max = df_salary_zhaopin['Max Salary'].apply(int_x)
    # df_max = df_max.rename(columns={0:'Max Salary'})
    return df_min

def zhaopin_split_max(df_dm_zl):
    split = lambda x: pd.Series(x.split('-'))
    df_salary_zhaopin = df_dm_zl['salary'].apply(split)
    df_salary_zhaopin = df_salary_zhaopin.rename(columns={0:'Min Salary',1:'Max Salary'}).dropna()
    int_x = lambda x:pd.Series(str(int(x)/1000)+'k')
    # df_min = df_salary_zhaopin['Min Salary'].apply(int_x)
    # df_min = df_min.rename(columns={0:'Min Salary'})
    df_max = df_salary_zhaopin['Max Salary'].apply(int_x)
    df_max = df_max.rename(columns={0:'Max Salary'})
    return df_max

def lagou_average_salary_min(df_salary_lagou,df_min_lagou):
    for i in range(len(df_salary_lagou)):
        try:
            tmp = pd.Series([int(df_salary_lagou['Min Salary'][i].encode('utf-8').replace('k',''))])
            df_min_lagou = df_min_lagou.append(tmp)
        except:
            # print i
            pass
    return df_min_lagou

def lagou_average_salary_max(df_salary_lagou,df_max_lagou):
    for i in range(len(df_salary_lagou)):
        try:
            tmp_m = pd.Series([int(df_salary_lagou['Max Salary'][i].encode('utf-8').replace('k', ''))])
            df_max_lagou = df_max_lagou.append(tmp_m)
        except:
            # print i
            pass
    return df_max_lagou

def average_salary(df_da,df_dm_zl):
    str_to_num = lambda x: pd.Series(int(x.encode('utf-8').replace('k', '')))
    df_min_lagou = pd.Series()
    df_max_lagou = pd.Series()
    df_salary_lagou = lagou_split(df_da)
    df_min_lagou = lagou_average_salary_min(df_salary_lagou,df_min_lagou)
    df_max_lagou = lagou_average_salary_max(df_salary_lagou,df_max_lagou)

    df_min = zhaopin_split_min(df_dm_zl)
    df_max = zhaopin_split_max(df_dm_zl)

    df_min_zhaopin = df_min['Min Salary'].apply(str_to_num)
    df_max_zhaopin = df_max['Max Salary'].apply(str_to_num)

    average_max_lagou = df_max_lagou[0].mean()
    average_min_lagou = df_min_lagou[0].mean()
    average_max_zhaopin = df_max_zhaopin[0].mean()
    average_min_zhaopin = df_min_zhaopin[0].mean()

    average_min_salary = [average_min_lagou,average_min_zhaopin]
    average_max_salary = [average_max_lagou,average_max_zhaopin]
    return [average_min_salary,average_max_salary]

salary_data = average_salary(df_da,df_dm_zl)
salary_sh = average_salary(df_sh,df_sh_zl)
salary_bj = average_salary(df_bj,df_bj_zl)
salary_gz = average_salary(df_gz,df_gz_zl)

salary_it = average_salary(df_it,df_it_zl)

salary_ug = average_salary(df_ug,df_ug_zl)
salary_ms = average_salary(df_ms,df_ms_zl)
salary_ph = average_salary(df_ph,df_ph_zl)
