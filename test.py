import os, itertools
from lib import LSM

for root, dirs, files in os.walk('data'):
    folks = {}
    for folk in files:
    	with open(os.path.join(root, folk), 'r') as f:
    		folks[folk] = LSM(f.read())

combos = itertools.combinations(folks.items(), 2)
compares = []
everybody = sum(folks.values())
for obj1, obj2 in [combo for combo in combos]:
	compares.append([obj1[0], obj2[0], 
		str(obj1[1].compare(obj2[1])),
		str(obj1[1].compare(everybody))])

print "who is most like each other"
compares.sort(key=lambda x:x[2])
compares.reverse()
for row in compares:
	print row[:-1]

print "who is most like the average"
compares.sort(key=lambda x:x[3])
compares.reverse()
printed = []
for row in compares:
	to_print = [row[0], row[3]]
	if to_print not in printed: print to_print
	printed.append(to_print)
