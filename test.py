import accounts
import twitter_api

ta = twitter_api.TwitterApi('renxia.wang')
#print ta.is_oauth_successed()
#print ta.get_user_profile(uid=396943519)
print ta.get_user_tweets(uid=396943519)
#print ta.get_user_followings(uid=396943519)
