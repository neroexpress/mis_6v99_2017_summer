# The code starts from here.

import requests;from itertools import combinations;import pprint

training_url  = "http://kevincrook.com/utd/market_basket_training.txt"
test_url = "http://kevincrook.com/utd/market_basket_test.txt"
training_file="market_basket_training.txt"
test_file = "market_basket_test.txt"

product_list = ['P01', 'P02', 'P03', 'P04','P05', 'P06', 'P07', 'P08','P09','P10']

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

def get_valid_four_digitlist(product_list):
	possible_combinations = [list(combinations(product_list, i)) for i in range(len(product_list)+1)]
	valid_combinations = [ls for ls in possible_combinations if len(ls[0])>0 and len(ls[0])<5]
	fourdigit_productlist = list()
	for x in valid_combinations:
		[fourdigit_productlist.append(list(i)) for i in x]
	#pprint.pprint(fourdigit_productlist)
	return fourdigit_productlist

#get_training_set(training_url,training_file)
#get_test_data(test_url,test_file)

#fourdigit_productlist = get_valid_four_digitlist(product_list)







