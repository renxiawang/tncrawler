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
        time.sleep(61)
        continue

      self.db.insert_following(uid, followings)
        
      self.visited_followings_queue.put(uid)
      # add ids to task queues
      for id in followings:
        if not self.is_repeated(id):
          self.profiles_queue.put(id)
          self.followings_queue.put(id)

      self.db.update_following_progress(self.followings_queue, self.visited_followings_queue)
      time.sleep(61)

  def is_repeated(self, uid):
    if uid in self.visited_profiles_queue.queue and uid in self.profiles_queue.queue and uid in self.visited_followings_queue.queue and uid in self.followings_queue.queue:
      return True
    return False

class Crawler(object):
  def __init__(self, users = None, followings = None):
    self.visited_profiles_queue = Queue()
    self.visited_followings_queue = Queue()

    self.profiles_queue = Queue()
    self.followings_queue = Queue()

    for u in users:
      self.profiles_queue.put(u)
    for f in followings:
      self.followings_queue.put(f)

  def start(self):
    profile_thread = ProfileThread('Pro', self.profiles_queue, self.visited_profiles_queue)
    following_thread = FollowingThread('Fol', self.followings_queue, self.profiles_queue, self.visited_followings_queue, self.visited_profiles_queue)

    following_thread.start()
    profile_thread.start()
    
    following_thread.join()
    profile_thread.join()

    print "ALL DONE!"
