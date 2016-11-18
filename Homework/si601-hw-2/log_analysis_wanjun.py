__author__ = 'wanjun'

import re
from collections import Counter

acess_log = open('access_log.txt','rU')

pattern1 = r'^\S+ . . \[(.+)\] "(.*)" (\d+) \S+ "(.*)" ".*"'
pattern2 = r'(GET|POST) (http|https)?:\/\/[a-zA-Z]'
pattern3 = r'\d{2}\/\w{3}\/\d{4}'
i = 1
dat_dic = dict()
inv_log = []
for log in acess_log:
    match1 = re.search(pattern1, log)
    if ('GET' in match1.group(2) or 'POST' in match1.group(2)) and match1.group(3) == '200':
        if re.match(pattern2,match1.group(2)):
            temp = re.search(r'https?:\/\/[a-zA-Z]([\w\.-])+(?<=\.)([a-zA-Z]+)(.+)?',match1.group(2))
            date = re.search(pattern3,match1.group(1))
            try:
                if date.group() in dat_dic:
                    dat_dic[date.group()] = str(temp.group(2)).lower() + ' ' + dat_dic[date.group()]
                else:
                    dat_dic[date.group()] = str(temp.group(2)).lower()
            except:
                inv_log.append(log)
                i += 1
        else:
            inv_log.append(log)
            i += 1
    else:
        inv_log.append(log)
        i += 1

inv_dat = open('invalid_access_log_wanjun.txt', 'w')
for k in range(len(inv_log)):
    inv_dat.write(inv_log[k])
inv_dat.close()

log_sum = open('valid_log_summary_wanjun.txt', 'w')
for key in sorted(dat_dic):
    log_dict = dict((Counter(dat_dic[key].split()).items()))
    log_sum.write(key)
    for key2 in sorted(log_dict):
        log_sum.write('\t' + key2 + ':' + str(log_dict[key2]))
    log_sum.write('\n')
log_sum.close()
