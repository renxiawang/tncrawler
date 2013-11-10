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
      print '%s failed because of %s' % (uid, e.reason)

    return user_proile

  def get_user_followings(self, uid=None, sname=None):
    friends_ids = []

    try:
      # friends_ids = self.api.friends_ids(user_id=uid, screen_name=sname)['ids']
      # print "get", len(friends_ids), "followings of ", uid
      # time.sleep(60)
      
      for friends in tweepy.Cursor(self.api.friends_ids, user_id=uid, screen_name=sname).pages():
        print "crawling followings:", uid
        friends_ids.extend(friends['ids'])
        time.sleep(60)

    except tweepy.error.TweepError, e:
      friends_ids = None
      print '%s failed because of %s' % (uid, e.reason)
      time.sleep(60)  
    
    return friends_ids

  def get_user_followers(self, uid=None, sname=None):
    followers_ids = []

    try:
      # followers_ids = self.api.followers_ids(user_id=uid, screen_name=sname)['ids']
      # print "get", len(followers_ids), "followers of ", uid
      # time.sleep(60)
      
      for follower in tweepy.Cursor(self.api.followers_ids, user_id=uid, screen_name=sname).pages():
        print "crawling followers:",uid
        followers_ids.extend(follower['ids'])
        time.sleep(60)

    except tweepy.error.TweepError, e:
      followers_ids = None
      print '%s failed because of %s' % (uid, e.reason)
      time.sleep(60) 
    
    return followers_ids

