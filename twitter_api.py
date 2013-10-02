#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import tweepy
from tweepy.parsers import JSONParser

class TwitterApi(object):

  def __init__(self):
    self.consumer_key = 'BfdpgMeDAzqNIixHhLjQ'
    self.consumer_secret = 'wfYF8Tp4uSJ3nGgqe5yGB1Wn6XOX8MYC5vcuavXBpsU'
    self.access_token = '153077173-bAfnlt3NJEGj6KDE8BDYq93GCJ3omoZMtJreqoU9'
    self.access_secret = 'x2eMIdu5AK02bLldfE7gxVYdnsnLRIUXwWrDoxAo'

    self.auth = tweepy.auth.OAuthHandler(self.consumer_key, self.consumer_secret)
    self.auth.set_access_token(self.access_token, self.access_secret)
    self.api = tweepy.API(self.auth, parser=JSONParser())

  def is_oauth_successed(self):
    verify_credentials = None
    try:
      verify_credentials = self.api.verify_credentials()
    except tweepy.error.TweepError, e:
      print 'failed because of %s' % e.reason
    
    return verify_credentials

  def get_user_profile(self, uid):
    user_proile = None
    try:
      user_proile = self.api.get_user(uid)
    except tweepy.error.TweepError, e:
      print '%d failed because of %s' % (uid, e.reason)

    return user_proile

  def get_user_followings(self, uid=None, sname=None):
    friends_ids = []

    try:
      for friends in tweepy.Cursor(self.api.friends_ids, user_id=uid, screen_name=sname).pages():
        friends_ids.extend(friends['ids'])
        time.sleep(60)

    except tweepy.error.TweepError, e:
      friends_ids = None
      print '%d failed because of %s' % (uid, e.reason)
      time.sleep(60)  
    
    return friends_ids

  def get_user_followers(self, uid=None, sname=None):
    followers_ids = []

    try:
      for follower in tweepy.Cursor(self.api.followers_ids, user_id=uid, screen_name=sname).pages():
        followers_ids.extend(follower['ids'])
        time.sleep(60)

    except tweepy.error.TweepError, e:
      followers_ids = None
      print '%d failed because of %s' % (uid, e.reason)
      time.sleep(60) 
    
    return followers_ids

  def get_user_id_by_screen_name(self, snames):
    snames = ['graceishuman','Luvvie','Scandalminute','goldietaylor','blackcanseco','youngsinick','karnythia','profblmkelley','LacharlesWard','drgoddess','GeeDee215','ladyknight33','Mrs_Amelia','MisJia','NeoScandal','C_ozzy8','dtburnetsky','PINKJUNKI','deborah91473','abbims']
    for name in snames:
      try:
        u = self.api.get_user(screen_name=name)
        print u['id']
        time.sleep(5)
      except tweepy.error.TweepError, e:
        print "Exception:", name, e.reason
        time.sleep(5)