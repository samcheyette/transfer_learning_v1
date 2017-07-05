
from helpers import *
import os


if __name__ == "__main__":
	CHAINS= 3
	STEPS = 15000
	PRIOR_TEMP = 0.85
	TOPN=100
	ALPHA = 1.0-1.0e-4
	#how much generalization do we need?
	REQUIRE_N = 1
	WHICH = "none"

	output="out2.csv"

	data = vanilla_conditions()
	#print data
	
	to_call = "python rrules_reuse_mcmc.py "
	to_call += "%d %d %d %f %f %d %s %s " % (CHAINS, STEPS, TOPN, PRIOR_TEMP,
									ALPHA, REQUIRE_N, WHICH , output)


	if WHICH == 'none':
		data = [data[0]] + [data[6]]

	for k in data:
		#print k
	#run_wrapper(data, which="reuse")

		os.system(to_call + k)	