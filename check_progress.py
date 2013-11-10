from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.scandal_network
profile = db.profile

print "Profiles: ", profile.find({"profile":{"$exists":True}}).count()
print "Followings: ", profile.find({"following_ids":{"$exists":True}}).count()
print "Followers: ", profile.find({"follower_ids":{"$exists":True}}).count()

