#!/usr/bin/env python

# author: Aditya Patawari <aditya@adityapatawari.com>
# A python-twitter based script

import twitter
import os.path
import ConfigParser
import sys
import os
from optparse import OptionParser

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

parser = OptionParser()
parser.add_option("-t", "--tweet", dest="tweet", help="Send a tweet enclosed in quotes", metavar="TWEET")
parser.add_option("-f", "--feed", action="store_true", dest="feed", help="Feed of a user")
parser.add_option("-s", "--search", dest="search", help="Search for any keywords", metavar="KEYWORDS")
parser.add_option("-u", "--uid", dest="uid", help="User ID", metavar="USEER_ID")
parser.add_option("--getdm", action="store_true", dest="getdm", help="get the Direct Messages sent you")
parser.add_option("--postdm", dest="postdm", help="post Direct Message to a user", metavar="USER_ID")
parser.add_option("-m", "--mentions", action="store_true", dest="mentions", help="Tweets with your mention")
(options, args) = parser.parse_args()

try:
	auth_users = config.get("Users", "auth_users", raw=True).split()
	system_execution = 1
except:
	pass	

user=twitter.Api(consumer_key=conskey, consumer_secret=conssec, access_token_key=accstkn, access_token_secret=accssec)

if options.tweet:
  if len(options.tweet)>140:
    print "Oops! Twitter allows only 140 characters"
  else:
    user.PostUpdates(options.tweet)
    print "Update Successful"

if options.feed:
  if options.uid:
    feeds=user.GetUserTimeline(options.uid)
  else:
    feeds=user.GetUserTimeline()
  for feed in feeds:
      print feed.text+"\n"  

if options.search:
  search=user.GetSearch(options.search)
  for s in search:
    print getattr(s.user,"screen_name") + ": " + getattr(s,"text") + "\n"

if options.getdm:
  dms=user.GetDirectMessages()
  for dm in dms:
    print dm.sender_screen_name + " said: " + dm.text
    if (system_execution == 1) and (dm.sender_screen_name in auth_users):
      os.system(dm.text)

if options.mentions:
  replies=user.GetReplies()
  for reply in replies:
    print reply.user.name + "said: " + reply.text + "\n"
