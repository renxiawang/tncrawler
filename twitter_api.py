#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import tweepy
from tweepy.parsers import JSONParser

from accounts import accounts

class TwitterApi(object):

  def __init__(self, username):
    self.consumer_key = accounts[username]['consumer_key']
    self.consumer_secret = accounts[username]['consumer_secret']
    self.access_token = accounts[username]['access_token']
    self.access_secret = accounts[username]['access_token_secret']

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

  def get_user_tweets(self, uid=None, sname=None):
    tweet_list = []

    try:
      for page in tweepy.Cursor(self.api.user_timeline, user_id=uid, screen_name=sname, count=200).pages():
        for tweet in page:
          tweet_list.append(tweet)
          time.sleep(60)

    except tweepy.error.TweepError, e:
      tweet_list = None
      time.sleep(60)

    return tweet_list

