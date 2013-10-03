#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from crawler import Crawler

def load_user_list():
  file_name = sys.argv[1]
  user_list = []
  
  try:
    f = open(file_name, "r")
    for line in f.readlines():
      user_list.append(int(line.strip()))
  except Exception, e:
    raise e
    user_list = None

  return user_list

def main():
  user_list = load_user_list()
  if user_list:
    crawler = Crawler(user_list, None, user_list, None, user_list, None)
    crawler.start()

if __name__ == '__main__':
  main()