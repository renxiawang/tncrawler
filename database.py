#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Database Module

"""

from pymongo import MongoClient

class Database(object):
  def __init__(self):
    self.client = MongoClient('localhost', 27017)
    self.db = self.client.twitter_network
    self.profile = self.db.profile
    self.progress = self.db.progress
    self.failure = self.db.failure
  
  def insert_profile(self, profile):
    self.profile.update({"uid":profile['id']}, {"$set":{"profile":profile}}, upsert = True)

  def insert_following(self, uid, following_ids):
    self.profile.update({"uid":uid}, {"$set": {"following_ids": list(following_ids)}}, upsert = True)

  def insert_follower(self, uid, follower_ids):
    self.profile.update({"uid":uid}, {"$set": {"follower_ids": list(follower_ids)}}, upsert = True)

  def update_profile_progress(self, profiles_queue, visited_profiles_queue):
    doc = {
    "profiles_queue" : list(profiles_queue.queue),
    "visited_profiles_queue" : list(visited_profiles_queue.queue)
    }
    self.progress.update({"_id": 1}, {"$set" : doc}, upsert = True)

  def update_following_progress(self, followings_queue, visited_followings_queue):
    doc = {
    "followings_queue" : list(followings_queue.queue),
    "visited_followings_queue" : list(visited_followings_queue.queue)
    }
    self.progress.update({"_id": 2}, {"$set" : doc}, upsert = True)

  def update_follower_progress(self, followers_queue, visited_followers_queue):
    doc = {
    "followers_queue" : list(followers_queue.queue),
    "visited_followers_queue" : list(visited_followers_queue.queue)
    }
    self.progress.update({"_id": 3}, {"$set" : doc}, upsert = True)

  def record_failure(self, failed_proile = None, failed_following = None, failed_follower = None):
    if failed_proile:
      self.failure.update({"_id":1}, {"$addToSet":{"failed_proile":failed_proile}}, upsert = True)
    elif failed_following:
      self.failure.update({"_id":1}, {"$addToSet":{"failed_following":failed_following}}, upsert = True)
    else:
      self.failure.update({"_id":1}, {"$addToSet":{"failed_follower":failed_follower}}, upsert = True)

  def close(self):
    self.client.close()