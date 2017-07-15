import numpy as np
a = np.arange(15).reshape(3,5)

file_name = "demo_numpy.txt"

list_of_values = list()
list_of_values.extend((a,a.shape,a.size,a.itemsize,a.ndim,a.dtype))

def print_to_textfile(fn,list_of_values):
	with open(fn,'wt') as f:
		for s in list_of_values:
			#print(s)
			print(s, file=f)

print_to_textfile(file_name,list_of_values)