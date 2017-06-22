from run_mcmc import *
import time

t_start = time.time()

CHAINS=1
STEPS = 3501

TOPN=10
ALPHA = 1.0-1.0e-3

#how much generalization do we need?
# (REQ_N=15 would require sequences > length-15)
REQUIRE_N = 1


conditions = vanilla_conditions()

#hypotheses = list(set([MyHypothesis() for _ in xrange(1000)]))


##############################################################
##############RUN MCMC TO GET HYPOTHESES#####################

hypotheses = []
seen = set()
for condition in conditions:
	for d in xrange(len(condition)):
		data = condition[0:d]
		if data not in seen:
			r = run(data, CHAINS, STEPS, TOPN, ALPHA, REQUIRE_N)
			for h in r:
				hypotheses.append(h[0])
			seen.add(data)
hypotheses = list(set(hypotheses))

print len(hypotheses)
print time.time() - t_start
##############################################################
###################GET RULES##################################

from LOTlib.GrammarInference.Precompute import create_counts

which_rules = [r for r in grammar if r.nt not in ['START']]

counts, sig2idx, prior_offset = create_counts(grammar, hypotheses, which_rules=which_rules)

##############################################################
#####################GET HUMAN YN COUNTS######################



data_dct = get_training_data("data/outR.csv")
N0 = []
N1 = []
conditions = []
for d in data_dct:
	conditions.append(d)
	N0.append(data_dct[d][0])
	N1.append(data_dct[d][1])

##############################################################
#####################GET MOD YN PROB##########################


L = []
output = []

for h in xrange(len(hypotheses)):
	hyp = hypotheses[h]

	for datum in conditions:
		predll = (hyp.compute_likelihood([FunctionData(alpha=ALPHA,
					 require_n=REQUIRE_N,
					input=(), output={datum: len(datum)})]))
		h_out = hyp()
		if len(h_out) <= len(datum):
			output.append(0.5)
		else:
			if h_out[len(datum)] == '1':
				output.append(ALPHA)
			else:
				output.append(1.0 - ALPHA)
			#print hyp
			#print predll

			#print datum
			#print h_out
			#print h_out[len(datum)]
			#print

		L.append(predll)


################################################################
#####################EXPORT TO H5 FILE##########################

print time.time() - t_start

import h5py
import numpy

# stack together counts
kys = counts.keys()
ntlen = [len(counts[k][0]) for k in kys] # store how long each
counts = numpy.concatenate([counts[k] for k in kys], axis=1)
NHyp = len(hypotheses)

print "const int NRULES = %s;" % sum(ntlen)
print "const int NHYP = %s;" % NHyp
print "const int NDATA = %s;" % len(N1)
print "const int NNT = %s;" % len(ntlen)
print "const int NTLEN[NNT] = {%s};" % ','.join(map(str,ntlen))

# print out the key for understanding the columns
sigs = sig2idx.keys()
for k in kys:
    s = [sig for sig in sigs if sig[0] == k]
    s = sorted(s, key=sig2idx.get)
    for si in s:
        print sig2idx[si], si

# export as hdf5
with h5py.File('data.h5', 'w') as hf:
	# first write the 'specs'
	hf.create_dataset('specs',    data=[NHyp, sum(ntlen), len(N1), len(ntlen)], dtype=int)
	# write all the data
	hf.create_dataset('counts',    data=numpy.ravel(counts[:NHyp ], order='C'), dtype=int) # must be sure if we stop early, we don't include too many counts
	hf.create_dataset('output',    data=output, dtype=float)
	hf.create_dataset('human_yes', data=numpy.ravel(N1, order='C'), dtype=int)
	hf.create_dataset('human_no',  data=numpy.ravel(N0, order='C'), dtype=int)
	hf.create_dataset('likelihood',  data=numpy.ravel(L, order='C'), dtype=float)
	hf.create_dataset('ntlen', data=ntlen, dtype=int)
