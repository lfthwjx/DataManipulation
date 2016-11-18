#!/usr/bin/python -tt
"""
Created on Sep. 10th

@ author Jun Wang (wanjun)
"""
import csv
import math

#Step 1: Processing the input file
wb_ind = open("world_bank_indicators.txt", 'rU')
wb_ind_names = wb_ind.readline().split('\t')
wb_ind_value = []

for indrow in wb_ind:
    indwt = indrow.split('\t')
    indict = dict()
    if '2000' in indwt[1] or '2010' in indwt[1]:
        indict['Country Name'] = indwt[0]
        indict['Date'] = indwt[1]
        indict['Total population'] = indwt[9].strip('"')
        indict['Mobile subscribers'] = indwt[4].strip('"')
        indict['Health: mortality under-5'] = indwt[6]
        indict['Internet users per 100 people'] = indwt[5]
        indict['GDP per capita'] = indwt[19].replace('\n','').strip('"')
        if not ('' in indict.values()):
            indict['Mobile subscribers per capita'] = '{:.5f}'.format(float(indwt[4].replace(',','').strip('"'))/float(indwt[9].replace(',','').strip('"')))
            indict['log(GDP per capita)'] = '{:.5f}'.format(math.log(int(indwt[19].replace(',','').strip('\n').strip('"'))))
            indict['log(Health: mortality under 5)'] = '{:.5f}'.format(math.log(int(indwt[6].replace(',','').strip('"').strip('\n'))))
            wb_ind_value.append(indict)

#Step 2: Adding regions
wb_reg = open("world_bank_regions.txt",'rU')
wb_reg_names = wb_reg.readline().split('\t')
wb_reg_value = []

con_reg = dict()
for regrow in wb_reg:
    regdict = regrow.split('\t')
    con_reg[regdict[2].replace('\n','')] = regdict[0]

#Adding regions for the two countries missing their regions
con_reg['West Bank and Gaza'] = 'Asia'
con_reg['Tuvalu'] = 'Oceania'
    
for indcon in wb_ind_value:
    try:
        indcon['Region'] = con_reg[indcon['Country Name']]
    except:
        indcon['Region'] = ''

#Step 5: Sorting        
ind_reg_sorted = sorted(wb_ind_value, key = lambda x: (x['Date'][-4:],x['Region'],int(x['GDP per capita'].replace(',', ''))))
#Step 6: Output to a file in CSV format
colnames = ['Country Name', 'Date', 'Total population', 'Mobile subscribers', 'Health: mortality under-5', 'Internet users per 100 people', 'GDP per capita', 'Mobile subscribers per capita', 'log(GDP per capita)', 'log(Health: mortality under 5)', 'Region']

wb_csv = open('worldbank_output_wanjun.csv','wb')
wb_writer = csv.DictWriter(wb_csv, colnames)
wb_writer.writer.writerow(colnames)
wb_writer.writerows(ind_reg_sorted)

wb_csv.close()
wb_reg.close()
wb_ind.close()
