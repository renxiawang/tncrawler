#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import types
import threading
from Queue import Queue

from twitter_api import TwitterApi
from database import Database

class ProfileThread(threading.Thread):
  def __init__(self, thread_name, profiles_queue, visited_profiles_queue):
    threading.Thread.__init__(self, name=thread_name)
    self.api = TwitterApi()
    self.db = Database()
    self.profiles_queue = profiles_queue
    self.visited_profiles_queue = visited_profiles_queue

  def run(self):
    while self.profiles_queue.qsize() >= 0:
      if self.profiles_queue.qsize() == 0:
        time.sleep(120)
        continue

      print "%s Profiles Finished:\t\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.visited_profiles_queue.qsize())
      print "%s Profiles Left:\t\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.profiles_queue.qsize())
      
      uid = self.profiles_queue.get()
      user_profile = self.api.get_user_profile(uid)

      if user_profile == None:
        self.db.record_failure(failed_proile=uid)
      else:
        self.db.insert_profile(user_profile)
        self.visited_profiles_queue.put(uid)

      self.db.update_profile_progress(self.profiles_queue, self.visited_profiles_queue)
      time.sleep(6)

class FollowingThread(threading.Thread):
  def __init__(self, thread_name, followings_queue, profiles_queue, visited_followings_queue, visited_profiles_queue):
    threading.Thread.__init__(self, name=thread_name)
    self.api = TwitterApi()
    self.db = Database()
    self.followings_queue = followings_queue
    self.profiles_queue = profiles_queue
    self.visited_followings_queue = visited_followings_queue
    self.visited_profiles_queue = visited_profiles_queue 

  def run(self):
    while self.followings_queue.qsize() > 0:
      print "%s Followings Finished:\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.visited_followings_queue.qsize())
      print "%s Followings Left:\t\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.followings_queue.qsize())
      uid = self.followings_queue.get()

      if type(uid) is types.IntType:
        followings = self.api.get_user_followings(uid=uid)
      else:
        followings = self.api.get_user_followings(sname=uid)
      
      # download followings ids
      if followings == None:
        self.db.record_failure(failed_following=uid)
        # time.sleep(61)
        continue

      self.db.insert_following(uid, followings)
        
      self.visited_followings_queue.put(uid)
      # add ids to task queues
      for id in followings:
        if not self.is_in_profile_queue(id):
          self.profiles_queue.put(id)
        if not self.is_in_following_queue(id):
          self.followings_queue.put(id)

      self.db.update_following_progress(self.followings_queue, self.visited_followings_queue)
      # time.sleep(61)

  def is_in_profile_queue(self, uid):
    if uid in self.visited_profiles_queue.queue or uid in self.profiles_queue.queue:
      return True
    return False

  def is_in_following_queue(self, uid):
    if uid in self.visited_followings_queue.queue or uid in self.followings_queue.queue:
      return True
    return False

class FollowerThread(threading.Thread):
  def __init__(self, thread_name, followers_queue, profiles_queue, visited_followers_queue, visited_profiles_queue):
    threading.Thread.__init__(self, name=thread_name)
    self.api = TwitterApi()
    self.db = Database()
    self.followers_queue = followers_queue
    self.profiles_queue = profiles_queue
    self.visited_followers_queue = visited_followers_queue
    self.visited_profiles_queue = visited_profiles_queue 

  def run(self):
    while self.followers_queue.qsize() > 0:
      print "%s Followers Finished:\t\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.visited_followers_queue.qsize())
      print "%s Followers Left:\t\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.followers_queue.qsize())
      uid = self.followers_queue.get()

      if type(uid) is types.IntType:
        followers = self.api.get_user_followers(uid=uid)
      else:
        followers = self.api.get_user_followers(sname=uid)
      
      # download followers ids
      if followers == None:
        self.db.record_failure(failed_follower=uid)
        # time.sleep(61)
        continue

      self.db.insert_follower(uid, followers)
        
      self.visited_followers_queue.put(uid)
      # add ids to task queues
      for id in followers:
        if not self.is_in_profile_queue(id):
          self.profiles_queue.put(id)
        if not self.is_in_follower_queue(id):
          self.followers_queue.put(id)

      self.db.update_follower_progress(self.followers_queue, self.visited_followers_queue)
      # time.sleep(61)

  def is_in_profile_queue(self, uid):
    if uid in self.visited_profiles_queue.queue or uid in self.profiles_queue.queue:
      return True
    return False

  def is_in_follower_queue(self, uid):
    if uid in self.visited_followers_queue.queue or uid in self.followers_queue.queue:
      return True
    return False



class Crawler(object):
  def __init__(self, users = None, followings = None, followers = None):
    self.visited_profiles_queue = Queue()
    self.visited_followings_queue = Queue()
    self.visited_followers_queue = Queue()

    self.profiles_queue = Queue()
    self.followings_queue = Queue()
    self.followers_queue = Queue()

    for u in users:
      self.profiles_queue.put(u)
    for f in followings:
      self.followings_queue.put(f)
    for f in followers:
      self.followers_queue.put(f)

  def start(self):
    profile_thread = ProfileThread('Profi', self.profiles_queue, self.visited_profiles_queue)
    following_thread = FollowingThread('Fling', self.followings_queue, self.profiles_queue, self.visited_followings_queue, self.visited_profiles_queue)
    follower_thread = FollowerThread('Flwer', self.followers_queue, self.profiles_queue, self.visited_followers_queue, self.visited_profiles_queue)

    profile_thread.start()
    following_thread.start()
    follower_thread.start()
  
    profile_thread.join()
    following_thread.join()
    follower_thread.join()

    print "ALL DONE!"
