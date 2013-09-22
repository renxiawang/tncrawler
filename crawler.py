#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import deque
import time
import types

from twitter_api import TwitterApi
from database import Database

class ClassName(object):
  """docstring for ClassName"""
  def __init__(self, arg):
    super(ClassName, self).__init__()
    self.arg = arg
    

class Crawler(object):
  """docstring for Crawler"""
  def __init__(self, users = None, followings = None):
    self.api = TwitterApi()
    self.db = Database()

    self.is_first_time = True
    self.visited_profiles_set = set()
    self.visited_followings_set = set()

    self.unvisited_profiles_queue = deque()
    self.unvisited_following_queue = deque()

    if users:
      self.unvisited_profiles_queue.extend(users)
    if followings:
      self.unvisited_following_queue.extend(users)

  def start(self):
    if self.api.is_oauth_successed() == None:
      return

    total_sleep_time = 0
    while len(self.unvisited_profiles_queue) != 0 or len(self.unvisited_following_queue) != 0:
      print "Profiles Left:\t", len(self.unvisited_profiles_queue)
      print "Followings Left:\t", len(self.unvisited_following_queue)
      
      # GET users/show API limits one request per 5 second
      # Sleep 6 sec to ensure not exceeding the limitation
      time.sleep(6)
      total_sleep_time += 6

      # get user proile
      uid = self.unvisited_profiles_queue.popleft()
      user_profile = self.api.get_user_profile(uid)
      if user_profile == None:
        self.record_failure(failed_proile=uid)
      else:
        self.db.insert_profile(user_profile)
        self.visited_profiles_set.add(uid)

      # get user's followings
      if total_sleep_time > 60 or self.is_first_time:
        # backup progress
        self.backup_progress()

        uid = self.unvisited_following_queue.popleft()

        if type(uid) is types.IntType:
          followings = self.api.get_user_followings(uid=uid)
        else:
          followings = self.api.get_user_followings(sname=uid)

        # download followings ids
        if followings == None:
          self.record_failure(failed_following=uid)
          total_sleep_time = 0
          continue

        self.db.insert_following(uid, followings)
        
        self.visited_followings_set.add(uid)
        # add ids to task queues
        for id in followings:
          if not self.is_repeated(id):
            self.unvisited_profiles_queue.append(id)
            self.unvisited_following_queue.append(id)

        total_sleep_time = 0
        self.is_first_time = False

  def is_repeated(self, uid):
    if uid in self.visited_profiles_set and uid in self.unvisited_profiles_queue and uid in self.visited_followings_set and uid in self.unvisited_following_queue:
      return True
    return False

  def record_failure(self, failed_proile = None, failed_following = None):
    if failed_proile:
      self.db.record_failure(failed_proile=failed_proile)
    else:
      self.db.record_failure(failed_following=failed_following)

  def backup_progress(self):
    self.db.update_progress(self.unvisited_profiles_queue, self.unvisited_following_queue, self.visited_profiles_set, self.visited_followings_set)
