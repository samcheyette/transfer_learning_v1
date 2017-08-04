import os
from helpers import *

CHAINS=2
STEPS = 20000
TOPN=20000
ALPHA = 1.0-1.0e-3
REQUIRE_N = 1
DATA = vanilla_conditions(appstim=True,append=True)



for DATUM in DATA[1:]:
	#to_call = "python export_to_gpu.py "
	to_call = "python find_transformations.py "
	to_call += "%d %d %d %f %d %s " % (CHAINS, 
		STEPS, 
		TOPN,
		ALPHA, REQUIRE_N, DATUM)




	os.system(to_call)
