d1 = {1:{'a':1 , 'b':2}}
d2 = {'2' : {'c':3 , 'd':4}}

print(abd(d1,d2))

def abd(d1,d2):

	print("helloo")
	res= {**d1,**d2}
	return res
