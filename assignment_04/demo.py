
# coding: utf-8

# In[10]:

import tweepy
import json


# In[11]:

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, max_responses):
        self.max_responses = max_responses
        self.num_responses = 0
    def on_data(self, data):
        if self.num_responses == self.max_responses:
            return False
        self.num_responses +=1
        
        json_data = json.loads(data)
        
        
        print("\n\n")
        print("===============================")
        print("      ", self.num_responses)
        print("===============================")
        print(json.dumps(json_data, sort_keys = True, indent = 4)) # sort every order right
        
        if 'text' in json_data:
            print("\n\nTweet:",json_data['text'])
    def on_error(self, error_code):
        print("error:", error_code)
        if error_code == 420:
            print("rate limited")
            return False
        


# In[12]:

consumer_key = 'BkdSnSTpbLVaulDBgWfeKfwUv'
consumer_secret='ao0RU3Hbietr5C8JZsYXJDXm6DDVW2bNM5yeRiLfxW2ETRTYOa'
access_token='893620611477647362-deDwizqqgxBhn7myo4CAKmIJLHmgff9'
access_token_secret = 'PpUWK44QxVBxAZdQCAIY88gjEl85fYgrReLUgwuWnGWLR'


# In[13]:

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)


# In[14]:

my_stream_listener = MyStreamListener(5)


# In[15]:

my_stream = tweepy.Stream(auth=api.auth, 
                          listener = my_stream_listener,
                          timeout = 60,
                          wait_on_rate_limit = True
                         )


# In[19]:

my_stream.sample()


# In[7]:

my_stream.filter(track=('trump', 'clinton'))


# In[16]:

my_stream.filter(languages = ['en'], async=True)


# In[ ]:

json_data = json.load(f)
f.close()

f=open('tweets.txt',)

