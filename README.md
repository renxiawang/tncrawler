tncrawler
=========

A crawler for crawling user profiles, followings and followers on Twitter. 

#### Requires
1. [Tweepy](https://github.com/tweepy/tweepy)
2. [Pymongo](http://api.mongodb.org/python/current/installation.html)
3. [MongoDB](http://www.mongodb.org/)

#### Usages
To initial the crawling task, execute:

    python main.py user_list
where **user_list** is the file name of a text file that contains **user ids**. One **user id** per line. 

To continue the task after program crash, execute:

    python main_load.py

#### Todos
0. Complete the commond-line arguments processing function
1. Meet PEP8 Standard
2. Rewrite three thread classes; Consider a solution using thread pool 
3. Logging function
4. Combine main.py and main_load.py