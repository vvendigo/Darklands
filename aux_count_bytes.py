import sys

fname = sys.argv[1] # file to find in

data = map(ord, open(fname).read())

counter = [0]*256

for b in data:
	counter[b] += 1

m = float(max(counter))

for b, c in enumerate(counter):
	print "%3d: %8d %s"%(b, c, '#'*int(c/m*30))
