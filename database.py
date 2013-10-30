#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Database Module

"""

from pymongo import MongoClient

class Database(object):
  def __init__(self):
    self.client = MongoClient('localhost', 27017)
    self.db = self.client.twitter_network_new
    self.profile = self.db.profile
    self.progress = self.db.progress
    self.failure = self.db.failure
  
  def is_existed(self, uid, key):
    result = self.profile.find({"$and":[{"uid":uid},{key:{"$exists":True}}]})
    if result.count() == 0:
      return False
    return True    
  
  def insert_profile(self, profile):
    self.profile.update({"uid":profile['id']}, {"$set":{"profile":profile}}, upsert = True)

  def insert_following(self, uid, following_ids):
    self.profile.update({"uid":uid}, {"$set": {"following_ids": list(following_ids)}}, upsert = True)

  def insert_follower(self, uid, follower_ids):
    self.profile.update({"uid":uid}, {"$set": {"follower_ids": list(follower_ids)}}, upsert = True)

  def update_profile_progress(self, profiles_queue, visited_profiles_queue):
    doc = {
    "profiles_queue" : str(list(profiles_queue.queue)).strip('[]'),
    "visited_profiles_queue" : str(list(visited_profiles_queue.queue)).strip('[]')
    }
    try:
      self.progress.update({"_id": 1}, {"$set" : doc}, upsert = True)
    except:
      print "profile progress size too large"

  def update_following_progress(self, followings_queue, visited_followings_queue):
    doc = {
    "followings_queue" : str(list(followings_queue.queue)).strip('[]'),
    "visited_followings_queue" : str(list(visited_followings_queue.queue)).strip('[]')
    }
    try:
      self.progress.update({"_id": 2}, {"$set" : doc}, upsert = True)
    except:
      print "following progress size too large"

  def update_follower_progress(self, followers_queue, visited_followers_queue):
    doc = {
    "followers_queue" : str(list(followers_queue.queue)).strip('[]'),
    "visited_followers_queue" : str(list(visited_followers_queue.queue)).strip('[]')
    }
    try:
      self.progress.update({"_id": 3}, {"$set" : doc}, upsert = True)
    except:
      print "follower progress size too large"   

  def record_failure(self, failed_proile = None, failed_following = None, failed_follower = None):
    if failed_proile:
      self.failure.update({"_id":1}, {"$addToSet":{"failed_proile":failed_proile}}, upsert = True)
    elif failed_following:
      self.failure.update({"_id":1}, {"$addToSet":{"failed_following":failed_following}}, upsert = True)
    else:
      self.failure.update({"_id":1}, {"$addToSet":{"failed_follower":failed_follower}}, upsert = True)

  def load_progress(self):
    # profiles_queue = self.progress.find({"_id":1})[0]["profiles_queue"]
    # visited_profiles_queue = self.progress.find({"_id":1})[0]["visited_profiles_queue"]

    # followings_queue = self.progress.find({"_id":2})[0]["followings_queue"]
    # visited_followings_queue = self.progress.find({"_id":2})[0]["visited_followings_queue"]

    # followers_queue = self.progress.find({"_id":3})[0]["followers_queue"]
    # visited_followers_queue = self.progress.find({"_id":3})[0]["visited_followers_queue"]

    #profiles_queue = map(int, self.progress.find({"_id":1})[0]["profiles_queue"].split(','))
    #visited_profiles_queue = map(int, self.progress.find({"_id":1})[0]["visited_profiles_queue"].split(','))

    #followings_queue = map(int, self.progress.find({"_id":2})[0]["followings_queue"].split(','))
    #visited_followings_queue = map(int, self.progress.find({"_id":2})[0]["visited_followings_queue"].split(','))

    #followers_queue = map(int, self.progress.find({"_id":3})[0]["followers_queue"].split(','))
    #visited_followers_queue = map(int, self.progress.find({"_id":3})[0]["visited_followers_queue"].split(','))
    unvisited_profiles = []
    visited_profiles = []
    unvisited_followings = []
    visited_followings = []
    unvisited_followers = []
    visited_followers = []

    for p in self.profile.find():
      if 'profile' in p:
        visited_profiles.append(p['uid'])
      if 'following_ids' in p:
        visited_followings.append(p['uid'])
        if len(p['following_ids']) > 5000:
          unvisited_profiles.extend(p['following_ids'][:5000])
        else:
          unvisited_profiles.extend(p['following_ids'])
      if 'follower_ids' in p:
        visited_followers.append(p['uid'])
        if len(p['follower_ids']) > 5000:
          unvisited_profiles.extend(p['follower_ids'][:5000])
        else:
          unvisited_profiles.extend(p['follower_ids'])

    unvisited_followings = list(set(unvisited_profiles).difference(set(visited_followings)))
    unvisited_followers = list(set(unvisited_profiles).difference(set(visited_followers)))
    unvisited_profiles = list(set(unvisited_profiles).difference(set(visited_profiles)))   

    return unvisited_profiles, visited_profiles, unvisited_followings, visited_followings, unvisited_followers, visited_followers

  def close(self):
    self.client.close()
