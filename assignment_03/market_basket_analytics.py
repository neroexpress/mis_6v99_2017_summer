# The code starts from here.

import requests; from itertools import combinations; import pprint
from collections import Counter

training_url  = "http://kevincrook.com/utd/market_basket_training.txt"
test_url = "http://kevincrook.com/utd/market_basket_test.txt"
training_file="market_basket_training.txt"
test_file = "market_basket_test.txt"
file_name = 'market_basket_recommendations.txt'

product_list = ['P01', 'P02', 'P03', 'P04','P05', 'P06', 'P07', 'P08','P09','P10']

def get_training_data(training_url,training_file):
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
	valid_combinations = [ls for ls in possible_combinations if len(ls[0])>1 and len(ls[0])<5]
	fourdigit_productlist = list()
	for x in valid_combinations:
		[fourdigit_productlist.append(list(i)) for i in x]
	#pprint.pprint(fourdigit_productlist)
	return [' '.join(x) for x in fourdigit_productlist]

def get_transaction_list(training_file):
	with open(training_file) as f:
	    data = f.readlines()
	#pprint.pprint(fourdigit_productlist[:50:])
	#print()
	a = [x.strip() for x in data]
	#pprint.pprint(a[:10:])
	#print()
	b =  [' '.join(x.split(',')[1::]) for x in a]
	#pprint.pprint(b[:10:])
	return b

def get_test_list(test_file):
	with open(test_file) as f:
	    data = f.readlines()
	#pprint.pprint(fourdigit_productlist[:50:])
	#print()
	a = [x.strip() for x in data]
	#pprint.pprint(a[:10:])
	#print()
	b =  [' '.join(x.split(',')[1::]) for x in a]
	#pprint.pprint(b[:10:])
	return b

get_training_data(training_url,training_file)
get_test_data(test_url,test_file)

#fourdigit_productlist = get_valid_four_digitlist(product_list)
transaction_productlist=get_transaction_list(training_file)
test_productlist=get_test_list(test_file)

#pprint.pprint(fourdigit_productlist[:10:])
#pprint.pprint(transaction_productlist[:10:])
#pprint.pprint(test_productlist[:10:])

transaction_productlist_count = Counter(transaction_productlist)
#pprint.pprint(transaction_productlist_count)

def print_suggested_product(fn, prod_list):
    with open(fn,'wt') as f:
        for s in prod_list:
            print(','.join(s), file=f)

def get_suggested_tuple(list_val):
	counts = list()
	for x in list_val:
		counts.append((x,transaction_productlist_count[x]))
	sorted_counts = sorted(counts, key=lambda tup: tup[1])
	#pprint.pprint(sorted_counts)
	return sorted_counts[-1]

def get_suggested_product(actual_prod,suggested_tuple):
	if suggested_tuple[1] != 0:
		actual_prod = actual_prod.split(' ')
		suggested_tuple = suggested_tuple[0].split(' ')
		item3 = [item for item in suggested_tuple if item not in actual_prod][0]
		#print(actual_prod,suggested_tuple,item3)
	else:
		item3 = ' '
	return item3

suggested_product_list = list()
product_number = 1
for i in test_productlist:
	list_val = list()
	#print(i)
	j = i.split(' ')
	k = [ix for ix in j if ix not in ['P04','P08']]
	#print(' '.join(k))
	product_list_local = [x for x in product_list if x not in k]
	list_val = [' '.join(k)+' '+x_val for x_val in product_list_local]
	#print(list_val)
	arranged_list = [' '.join(sorted(x.split(' '))) for x in list_val]
	#print(arranged_list)
	#print()
	suggested_tuple = get_suggested_tuple(arranged_list)
	suggested_product = get_suggested_product(i, suggested_tuple)
	suggested_product_list.append([str(product_number).rjust(3,'0'), suggested_product])
	product_number+=1

#pprint.pprint(suggested_product_list)
print_suggested_product(file_name, suggested_product_list)

