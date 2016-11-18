# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 00:55:55 2016

@author: Jun Wang
"""

s=' _ af44S '

def first_last_parts(s):
    stmp = s.strip()
    stmp = stmp.lower()
    stmp = stmp.replace(' ', '_')
    if len(stmp) < 5:
        return stmp
    elif stmp.isdigit():
        return stmp
    else:
        return stmp[0:2] + stmp[-2:]

first_last_parts(s)

#count = 4
#range(count)
#s[1:len(s)-1]
count=16
def bananas(count):
    if count==0:
        return 'no bananas'
    elif count==1:
        return 'a banana'
    elif count<6:
        bananaLoop = ''
        for i in range(count):
            bananaLoop = bananaLoop + str(i+1) + ' banana, '
        return bananaLoop[1:len(bananaLoop)-2]
    else:
        bananaLoop = '1 banana, 2 banana, 3 banana, 4 banana, 5 banana and ' + str(count-5) + ' more bananas'
        return bananaLoop
        
bananas(16)   


def match_ends(words, starting, ending):
    stawith=[]
    endwith=[]
    for word in words:
        if len(word)>=6: 
            if word.startswith(starting):
                 stawith.append(word)
            if word.endswith(ending):
                 endwith.append(word)
    staset = set(stawith)  
    endset = set(endwith)
    desiredwords = staset.intersection(endset)
    return len(desiredwords)
        
match_ends(['aerobiology', 'neurology', 'aerogy', 'anthropology', 'aerobiology', 'neurology', 'aerogy', 'anthropology'], 'a', 'ology')        


words = ['Microsoft', 'Intel', 'Intel', 'Intel', 'Apple', 'Apple']
#words.count('Intel')   
#countwords['Intel']
#countwords.items()     
def unique_counts(words):
    countwords = dict()
    for word in words:
        countwords[word] = words.count(word)
    result = sorted(countwords.items(), key = lambda wordcount: (-wordcount[1],wordcount[0]))
    return result
    
