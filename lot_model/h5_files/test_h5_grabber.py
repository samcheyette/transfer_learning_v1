import os
import re

all_files = os.listdir(".")
for f in all_files:
	if (os.path.isfile(f) and 
		re.match(".*?h5", f) != None and
		".h5" in str(f)):
		out = str(f)[:len(f)-3] + ".txt"
		call = "./in --in=%s > %s &" % (str(f), out)
		os.system(call)

