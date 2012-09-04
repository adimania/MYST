#!/usr/bin/env python

# author: Aditya Patawari <aditya@adityapatawari.com>
# A python-twitter based script

import twitter
import os.path
import ConfigParser
import sys
import os

__author__ = "Aditya Patawari <aditya@adityapatawari.com>"
version = 0.25

Description=''' MYST, short for My Status, is an ideal tool for status updates, DMs, searching etc.
It does everything a normal user can expect.
The Consumer Key and Secret Pair and Access Token Key and secret pair are stored in ~/.myst.conf
The format for the file is : 
    [MYST]
    consumer_key: <Consumer Key>
    consumer_secret: <Consumer Secret>
    access_token: <Access Token Key>
    access_token_secret: <Access Token Secret>
'''

Usage='''Usage: myst.py command
     tweet/update <update>			: Updates your status with "update"
     feed [username] <feed count>	: Gets the specified number of feed of the specified user '''
     
check = os.path.isfile(os.path.expanduser('~/.myst.conf'))
if cmp(check,False) == 0:
    print Description
    sys.exit(2)
    
system_execution = 0

config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.myst.conf'))
conskey = config.get("MYST", "consumer_key", raw=True)
conssec = config.get("MYST", "consumer_secret", raw=True)
accstkn = config.get("MYST", "access_token", raw=True)
accssec = config.get("MYST", "access_token_secret", raw=True)

try:
	auth_users = config.get("Users", "auth_users", raw=True).split()
	system_execution = 1
except:
	pass	

user=twitter.Api(consumer_key=conskey, consumer_secret=conssec, access_token_key=accstkn, access_token_secret=accssec)

if len(sys.argv)==1:
  print Usage
  sys.exit(2)
  

if (cmp(sys.argv[1], '-h') or cmp(sys.argv[1],'--help')) == 0:
  print Usage
  sys.exit(2)
    
if cmp(sys.argv[1], "update") == 0 or cmp(sys.argv[1], "tweet") == 0:
  status=' '.join(sys.argv[2:])
  if len(status) < 140:
    user.PostUpdates(status)
    print "Status Update Successful"
  else:
    print "The update is of " + str(len(status)) + " chars. Twitter does not allow more than 140 char"
  
if cmp(sys.argv[1], "mention") == 0:
  replies=user.GetReplies()
  for reply in replies:
    print reply.text

if cmp(sys.argv[1], "feed") == 0 and len(sys.argv) == 4:
  feeds=user.GetUserTimeline(sys.argv[2],count=sys.argv[3])
  for feed in feeds:
    print feed.text
  
elif cmp(sys.argv[1], "feed") == 0 and len(sys.argv)==3:
    feeds=user.GetUserTimeline(sys.argv[2])
    for feed in feeds:
      print feed.text
  
if cmp(sys.argv[1], "search") == 0:
  search=user.GetSearch(' '.join(sys.argv[2:]))
  for s in search:
    print getattr(s.user,"screen_name") + ": " + getattr(s,"text")
    
if cmp(sys.argv[1], "getdm") == 0:
	dms=user.GetDirectMessages()
	for dm in dms:
		print dm.sender_screen_name + " said: " + dm.text
		if (system_execution == 1) and (dm.sender_screen_name in auth_users):
			os.system(dm.text)
