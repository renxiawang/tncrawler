#!/usr/bin/python
# -*- coding: utf-8 -*-
from crawler import Crawler
from database import Database

def main():
  # user_list = load_user_list()
  db = Database()
  profiles_queue, visited_profiles_queue, followings_queue, visited_followings_queue, followers_queue, visited_followers_queue = db.load_progress()

  print "Load profiles queue: ", len(profiles_queue)
  print "Load visited profiles queue: ", len(visited_profiles_queue)
  print "Load followings queue: ", len(followings_queue)
  print "Load visited followings queue: ", len(visited_followings_queue)
  print "Load followers queue: ", len(followers_queue)
  print "Load visited followers queue: ", len(visited_followers_queue)
  
  crawler = Crawler(profiles_queue, visited_profiles_queue, followings_queue, visited_followings_queue, followers_queue, visited_followers_queue)
  crawler.start()

if __name__ == '__main__':
  main()
