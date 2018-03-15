import sys

fname = sys.argv[1] # file to find in
maxD = int(sys.argv[2]) # maximal distance between min & max found byte position in group
vals = map(int, sys.argv[3:]) # byte values to find (in any order)

chars = map(chr, vals)

data = open(fname).read()
dataLen = len(data)

pos = 0
lastPct = -1

while pos < dataLen:
	minP = dataLen
	maxP = pos
	for i, ch in enumerate(chars):
		p = data.find(ch, pos)
		if p < 0: sys.exit(0)
		minP = min(minP, p)
		maxP = max(maxP, p)
	#print minP, maxP
	d = maxP - minP
	if d <= maxD:
		print '%d:'%minP,
		for ch in data[minP:maxP+1]:
			if ch in chars:
				print '%3d#'%ord(ch),
			else:
				print '%3d '%ord(ch),
		print
	pos = minP+1
	pct = (float(pos)/dataLen)*100
	if lastPct != pct:
		#print "%3.3f"%(pct)
		lastPct = pct
		#if pct > 0.01: break
