# The code starts from here.

import requests; from itertools import combinations; from pprint import pprint
from collections import Counter; import json

JSON_file_url  = "http://kevincrook.com/utd/tweets.json"
JSON_file= "tweets_json_file.json"
twitter_anaytics_file = "twitter_analytics.txt"
Tweet_texts_file = "tweets.txt"

def download_JSON_file(JSON_file_url,JSON_file):
	r_training = requests.get(JSON_file_url)
	trainingf = open(JSON_file,"wb")
	trainingf.write(r_training.content)
	trainingf.close()

download_JSON_file(JSON_file_url,JSON_file)

def read_json_file(JSON_file):
	with open(JSON_file) as tweet_file:
		data = json.load(tweet_file)
	return data

json_data = read_json_file(JSON_file)
#pprint(json_data)

