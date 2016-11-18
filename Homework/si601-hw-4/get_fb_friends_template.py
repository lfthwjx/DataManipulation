# -*- coding: utf-8 -*-      
import facebook, urllib2, json, re, os
import sys

from time import sleep


### Example code to access the Facebook API
### Put your access token in the string variable:
access_token = '##REPLACE WITH YOUR ACCESS TOKEN ##'

### use Graph API to get friends
graph = facebook.GraphAPI(access_token)
profile = graph.get_object('me')
friends = graph.get_connections('me', 'friends')

for friend in friends['data']:
    ### get friend details
    response = urllib2.urlopen('https://graph.facebook.com/%s?access_token=%s&fields=gender,birthday,hometown,location,education,checkins' % (friend['id'], access_token))
    json_str = response.read()
    print json_str
    sleep(2)  # Pause between Facebook API calls
