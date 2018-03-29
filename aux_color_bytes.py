import sys

fname = sys.argv[1] # file to find in

data = map(ord, open(fname).read())

pal = ' .:*ijkbT?%&#$XW'

for b in data:
	sys.stdout.write(pal[b/16])

print
