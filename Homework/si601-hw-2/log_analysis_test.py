__author__ = 'wanjun'

import re
from collections import Counter

acess_log = open('access_log.txt','rU')

pattern1 = r'^\S+ . . \[(.+)\] "(.*)" (\d+) \S+ "(.*)" ".*"'
pattern2 = r'(GET|POST) (http|https)?:\/\/[a-zA-Z]'
pattern3 = r'\d{2}\/\w{3}\/\d{4}'
i = 1
datdom = dict()
invlog = []
for log in acess_log:
    match1 = re.search(pattern1, log)
    if ('GET' in match1.group(2) or 'POST' in match1.group(2)) and match1.group(3) == '200':
        if re.match(pattern2,match1.group(2)):
            temp = re.search(r'(http|https)?:\/\/[a-zA-Z]([\w\.-])+(?<=\.)([a-zA-Z]+)(.+)?',match1.group(2))
            date = re.search(pattern3,match1.group(1))
            try:
                if date.group() in datdom:
                    datdom[date.group()] = str(temp.group(2)).lower() + ' ' + datdom[date.group()]
                else:
                    datdom[date.group()] = str(temp.group(2)).lower()
            except:
                invlog.append(log)
                i += 1
        else:
            invlog.append(log)
            i += 1
    else:
        invlog.append(log)
        i += 1

invdat = open('invalid_access_log_wanjun.txt', 'w')
for k in range(len(invlog)):
    invdat.write(invlog[k])
invdat.close()

logsum = open('valid_log_summary_wanjun.txt', 'w')
for key in sorted(datdom):
    log_dict = dict((Counter(datdom[key].split()).items()))
    logsum.write( key )
    for key2 in sorted(log_dict):
        logsum.write('\t' + key2 + ':' + str(log_dict[key2]))
    logsum.write('\n')
logsum.close()
