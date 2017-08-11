# The code starts from here.

import requests; from itertools import combinations; from pprint import pprint
from collections import Counter; import json; import operator;import codecs

JSON_file_url  = "http://kevincrook.com/utd/tweets.json"
JSON_file= "tweets_json_file.json"
twitter_anaytics_file = "twitter_analytics.txt"
Tweet_texts_file = "tweets.txt"

def download_JSON_file(JSON_file_url,JSON_file):
	'''
	This function downloads the JSON data from the internet.
	'''
	r_training = requests.get(JSON_file_url)
	trainingf = open(JSON_file,"wb")
	trainingf.write(r_training.content)
	trainingf.close()

def read_json_file(JSON_file):
	'''
	This function reads the JSON file downloaded from the internet and returns a 
	python data structure.
	'''
	with open(JSON_file) as tweet_file:
		data = json.load(tweet_file)
	return data

def get_total_number_of_events(data):
	'''
	This function returns the total number of events in the twitter analytics file
	'''
	count = 0
	for x in data:
		count += 1
	return count

def get_total_number_of_tweets(data):
	'''
	This function retrieves the total number of tweets in the file.
	'''
	count=0
	for x in data:
		#if 'text' in x.keys():
		#	print('Text: {0}, Length: {1}'.format(x['text'].strip(),len(x['text'])))
		if 'text' in x.keys():
			count+=1
		#	print()
	return count


def get_lang_frequency(data):
	'''
	This function returns the language frequency of languages in tweets
	'''
	count=dict()
	for x in data:
		if 'text' in x.keys() and 'lang' in x.keys():
			key = x['lang']
			#print(key)
			count[key] = count.get(key,0) +1
	sorted_keys = sorted(count, key=count.get, reverse=True)
	frequency_list = list()
	for key in sorted_keys:
		frequency_list.append((key,count[key]))
	return frequency_list

def get_twitter_analytics_list(num_events,num_tweets,lang_freq):
	'''
	This function gives a list of values to print in twitter analytics file
	'''
	l = list()
	l.append(num_events)
	l.append(num_tweets)
	l.append(lang_freq)
	return l

def print_twitter_analytics(fn,list_value):
	'''
	This function prints the twitter analytics text file with various outputs
	'''
	with open(fn,'wt') as f:
		for s in list_value:
			if type(s) is not list:
				print(s,file=f)
			else:
				for x in s:
					li = [x[0],str(x[1])]
					print(','.join(li), file=f)

download_JSON_file(JSON_file_url,JSON_file)
json_data = read_json_file(JSON_file)
#pprint(json_data[702])

list_twitter_analytics = get_twitter_analytics_list(get_total_number_of_events(json_data),
							get_total_number_of_tweets(json_data),
							 get_lang_frequency(json_data))

print_twitter_analytics(twitter_anaytics_file,list_twitter_analytics)

#-------------------------------------------------------------------------------------------
#--------------------------- Print tweets.txt File -----------------------------------------
#-------------------------------------------------------------------------------------------


with codecs.open(Tweet_texts_file,'w',encoding='utf8') as f:
	'''
	This function writes all the tweet text to a text file using utf-8 encoding.
	'''
	#count = -1
	#t_count = -1
	for x in json_data:
		#t_count += 1
		if 'text' in x.keys():
			#count += 1
			#print("------------------------TOP-------------------------------------")
			#if count*2==1218:
			#	print(t_count)
			#	print(x['text'])
			#print("------------------------Below-------------------------------------")
			#print(count,file=f)
			print(x['text'].replace('\n', ' ').replace('\r', ''),file=f)


