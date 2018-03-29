import sys

fname = sys.argv[1] # file to find in

data = map(ord, open(fname).read())

for b in data:
	sys.stdout.write('%8s|'%(bin(b)[2:].replace('0',' ').replace('1','#')))

print
