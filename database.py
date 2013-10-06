#!/usr/bin/python
# -*- coding: utf-8 -*-
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

  def record_failure(self, failed_proile = None, failed_following = None, failed_follower = None):
    if failed_proile:
      self.failure.update({"_id":1}, {"$addToSet":{"failed_proile":failed_proile}}, upsert = True)
    elif failed_following:
      self.failure.update({"_id":1}, {"$addToSet":{"failed_following":failed_following}}, upsert = True)
    else:
      self.failure.update({"_id":1}, {"$addToSet":{"failed_follower":failed_follower}}, upsert = True)

  def load_progress(self):
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
        unvisited_profiles.extend(p['following_ids'])
      if 'follower_ids' in p:
        visited_followers.append(p['uid'])
        unvisited_profiles.extend(p['follower_ids'])

    unvisited_followings = list(set(unvisited_profiles).difference(set(visited_followings)))
    unvisited_followers = list(set(unvisited_profiles).difference(set(visited_followers)))
    unvisited_profiles = list(set(unvisited_profiles).difference(set(visited_profiles)))   

    return unvisited_profiles, visited_profiles, unvisited_followings, visited_followings, unvisited_followers, visited_followers

  def close(self):
    self.client.close()
