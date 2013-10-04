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
      
      uid = self.profiles_queue.get()
      user_profile = self.api.get_user_profile(uid)

      if user_profile == None:
        self.db.record_failure(failed_proile=uid)
        self.profiles_queue.task_done()
      else:
        self.db.insert_profile(user_profile)
        self.visited_profiles_queue.put(uid)
        
      self.db.update_profile_progress(self.profiles_queue, self.visited_profiles_queue)
      self.profiles_queue.task_done()

      print "%s Profiles Finished:\t\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.visited_profiles_queue.qsize())
      print "%s Profiles Left:\t\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.profiles_queue.qsize())
      time.sleep(5)

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
      uid = self.followings_queue.get()

      if type(uid) is types.IntType:
        followings = self.api.get_user_followings(uid=uid)
      else:
        followings = self.api.get_user_followings(sname=uid)
      
      # download followings ids
      if followings == None:
        self.db.record_failure(failed_following=uid)
        # time.sleep(61)
        self.followings_queue.task_done()
        continue

      self.db.insert_following(uid, followings)
        
      self.visited_followings_queue.put(uid)

      # add ids to task queues
      followings_for_profiles_queue = self.exclude_processed_profiles(followings)
      followings_for_followings_queue = self.exclude_processed_followings(followings)

      for id in followings_for_profiles_queue:
          self.profiles_queue.put(id)
      
      for id in followings_for_followings_queue:
          self.followings_queue.put(id)
      print "ing update progress"
      self.db.update_following_progress(self.followings_queue, self.visited_followings_queue)
      print "ing update progress end"
      self.followings_queue.task_done()

      print "%s Followings Finished:\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.visited_followings_queue.qsize())
      print "%s Followings Left:\t\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.followings_queue.qsize())
      # time.sleep(61)

  def exclude_processed_profiles(self, followings):
    profiles_set = set(self.visited_profiles_queue.queue).union(set(self.profiles_queue.queue))
    return set(followings).difference(profiles_set)

  def exclude_processed_followings(self, followings):
    followings_set = set(self.visited_followings_queue.queue).union(set(self.followings_queue.queue))
    return set(followings).difference(followings_set)


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
      uid = self.followers_queue.get()

      if type(uid) is types.IntType:
        followers = self.api.get_user_followers(uid=uid)
      else:
        followers = self.api.get_user_followers(sname=uid)
      
      # download followers ids
      if followers == None:
        self.db.record_failure(failed_follower=uid)
        self.followers_queue.task_done()
        # time.sleep(61)
        continue

      self.db.insert_follower(uid, followers)
        
      self.visited_followers_queue.put(uid)
      # add ids to task queues
      followers_for_profiles_queue = self.exclude_processed_profiles(followers)
      followers_for_followers_queue = self.exclude_processed_followers(followers)

      for id in followers_for_profiles_queue:
          self.profiles_queue.put(id)
      
      for id in followers_for_followers_queue:
          self.followers_queue.put(id)

      print "wer update progress"
      self.db.update_follower_progress(self.followers_queue, self.visited_followers_queue)
      print "wer update progress end"
      self.followers_queue.task_done()

      print "%s Followers Finished:\t\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.visited_followers_queue.qsize())
      print "%s Followers Left:\t\t %d" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.followers_queue.qsize())
      # time.sleep(61)

  def exclude_processed_profiles(self, followers):
    profiles_set = set(self.visited_profiles_queue.queue).union(set(self.profiles_queue.queue))
    return set(followers).difference(profiles_set)

  def exclude_processed_followers(self, followers):
    followers_set = set(self.visited_followers_queue.queue).union(set(self.followers_queue.queue))
    return set(followers).difference(followers_set)

class Crawler(object):
  def __init__(self, profiles = list(), visited_profiles = list(), followings = list(), visited_followings = list(), followers = list(), visited_followers = list()):
    self.visited_profiles_queue = Queue()
    self.visited_followings_queue = Queue()
    self.visited_followers_queue = Queue()

    self.profiles_queue = Queue()
    self.followings_queue = Queue()
    self.followers_queue = Queue()

    for p in profiles:
      self.profiles_queue.put(p)
    for vp in visited_profiles:
      self.visited_profiles_queue.put(vp)
    for f in followings:
      self.followings_queue.put(f)
    for vf in visited_followings:
      self.visited_followings_queue.put(vf)
    for f in followers:
      self.followers_queue.put(f)
    for vf in visited_followers:
      self.visited_followers_queue.put(vf)

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
