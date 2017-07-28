# The code starts from here.

import requests


training_url  = "http://kevincrook.com/utd/market_basket_training.txt"
test_url = "http://kevincrook.com/utd/market_basket_test.txt"

r_training = requests.get(training_url)
trainingf = open("training_data.txt","wb")
trainingf.write(r_training.content)
trainingf.close()

r_test = requests.get(test_url)
testf = open("test_data.txt","wb")
testf.write(r_test.content)
testf.close()