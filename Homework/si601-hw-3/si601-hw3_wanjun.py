#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json,urllib2,re,time,itertools,pydot
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
#step1

imdb = urllib2.urlopen('http://www.imdb.com/search/title?at=0&sort=num_votes&count=100')
imdb_html = imdb.read()
imdb_decoded = imdb_html.decode('utf-8')
imdb_encoded = imdb_decoded.encode('utf-8')
step1 = open('step1.html','w')
step1.writelines(imdb_encoded)
step1.close()

#step2
soup = BeautifulSoup(open('step1.html','r'))
contents = soup.find_all('a', {'href': re.compile('/title/.+/')})
years = soup.find_all('span',{'class':re.compile('lister-item-year')})

idnm = []
name = []
date = []
rank = []
for i in range(0,len(contents),3):
    idnm.append(contents[i+1].get('href').replace('/title/','').replace('/?ref_=adv_li_tt',''))
    name.append((contents[i+1].string).encode('utf-8'))
    date.append((years[i/3].string).encode('utf-8'))
    rank.append(str((i/3)+1))

step2 = open('step2.txt','w')
for j in range(len(name)):
    step2.write(idnm[j]+'\t'+rank[j]+'\t'+name[j]+date[j]+'\n')
step2.close()

#step3
'''
step3 = open('step3.txt','w')
i = 1
for id in idnm:
    md = urllib2.urlopen('http://www.omdbapi.com/?i=' + id)
    mddata = md.read().decode('utf-8')
    step3.write(mddata.encode('utf-8') + '\n')
    print str(i) + ' Completed'
    i += 1
    time.sleep(5)
step3.close()
'''

#step4
step4 = open('step4.txt','w')
json_data = open('step3.txt', 'rU')
for line in json_data :
    info = json.loads(line)
    # print info
    title = str(info['Title'].encode('utf-8'))
    actors = str(info['Actors'].encode('utf-8')).split(', ')
    json_actor = json.dumps(actors)
    step4.write(title + '\t' + json_actor + '\n')
step4.close()

#step5
step4 = open("step4.txt", "rU")
step4str = step4.readlines()
graph = pydot.Dot(graph_type='graph', charset="utf8")
for actors in step4str:
    #print actors
    #actor = actors.split('\t')
    actor = re.findall(r'".*"', actors)
    for one in actor:
        one = one.decode('utf8')
        one = one.replace('"', '')
        one = one.split(',')
        one = list(itertools.combinations(one, 2))
        for i in one:
            edge = pydot.Edge(i[0], i[1])
            graph.add_edge(edge)

graph.write('actors_graph_output.dot')