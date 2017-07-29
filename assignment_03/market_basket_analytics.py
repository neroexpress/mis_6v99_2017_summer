# The code starts from here.

import requests

training_url  = "http://kevincrook.com/utd/market_basket_training.txt"
test_url = "http://kevincrook.com/utd/market_basket_test.txt"
training_file="market_basket_training.txt"
test_file = "market_basket_test.txt"

def get_training_set(training_url,training_file):
	r_training = requests.get(training_url)
	trainingf = open(training_file,"wb")
	trainingf.write(r_training.content)
	trainingf.close()

def get_test_data(test_url,test_file):
	r_test = requests.get(test_url)
	testf = open(test_file,"wb")
	testf.write(r_test.content)
	testf.close()

#get_training_set(training_url,training_file)
#get_test_data(test_url,test_file)

