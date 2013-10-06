#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import tweepy
from tweepy.parsers import JSONParser

class TwitterApi(object):

  def __init__(self):
    self.consumer_key = 'UtIptL4lyPuXK8Nwbdf3rw'
    self.consumer_secret = 'UjZ4gpT9y8imJmh63uf528SpBLmE4K6XjkR9DKw8zkk'
    self.access_token = '1928368088-0Orce72vcWcRgXHrmxsU1vVNYUxfb3PUcGbL8y3'
    self.access_secret = 'l1JCaFALvn3pFrMXgq9JLL7l93atUxWPcCvBsuJDQ'

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
      for friends in tweepy.Cursor(self.api.friends_ids, user_id=uid, screen_name=sname).pages():
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
      for follower in tweepy.Cursor(self.api.followers_ids, user_id=uid, screen_name=sname).pages():
        followers_ids.extend(follower['ids'])
        time.sleep(60)

    except tweepy.error.TweepError, e:
      followers_ids = None
      print '%s failed because of %s' % (uid, e.reason)
      time.sleep(60) 
    
    return followers_ids
