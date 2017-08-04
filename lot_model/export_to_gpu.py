from run_mcmc import *
import time
import sys


t_start = time.time()

print sys.argv
class incr():
	def __init__(self):
		self.count=0

	def __call__(self):
		self.count+= 1
		return self.count

counter=incr()

CHAINS = int(sys.argv[counter()])
STEPS = int(sys.argv[counter()])
TOPN = int(sys.argv[counter()])
ALPHA = float(sys.argv[counter()])
REQUIRE_N = int(sys.argv[counter()])
conditioned_on =  sys.argv[counter()]
print CHAINS, STEPS, TOPN, ALPHA
#PRIOR_TEMP = float(sys.argv[counter()])

#REQUIRE_N = int(sys.argv[counter()])
lsts = vanilla_conditions(appstim=True,append=True)
full_lsts = vanilla_conditions_full(appstim=True, 
								append=True)

conditioned_on_full = None
for l in full_lsts:
	if l[:15] == conditioned_on:
		conditioned_on_full = [l]

print conditioned_on
assert(conditioned_on_full != None)
conditioned_on = [conditioned_on]

#how much generalization do we need?
# (REQ_N=15 would require sequences > length-15)



#lsts = ["101001010010100"]
#lsts = ["000000111111111", "111100000000000"]

#which to add to grammar
#conditioned_on = vanilla_conditions(appstim=True,append=False)
#conditioned_on_full = vanilla_conditions_full(appstim=True,append=False)

#conditioned_on = ["010110101101011"]
#conditioned_on_full = ["010110101101011010110101101011"]
#conditioned_on =      ["101001010010100"]
#conditioned_on_full = ["101001010010100101001010010100"]


#conditioned_on_full = ["100100010000100000100000010000"]




##############################################################
##############RUN MCMC TO GET HYPOTHESES#####################



def run_hyps(hypotheses):
	seen = set()
	for condition in list(set(conditioned_on + lsts)):
		for d in [6,10,15,15, 15]: #xrange(1,len(condition)+4,4):
			
			data = condition[0:d]
			if data not in seen:
				r = run(data, CHAINS, STEPS, TOPN, 
							ALPHA, REQUIRE_N,
							 PRIOR_TEMP=0.9)
				for h in r:
					hypotheses.append(h[0])
				seen.add(data)
	return hypotheses


#newT = "'%s'" % conditioned_on
#grammar.add_rule('TERM', newT, None, 10e-10)





#hypotheses = run_hyps([])
for l in conditioned_on_full:
	newT = "'%s'" % l
	grammar.add_rule('TERM', newT, None, 1e-2)
grammar.renormalize()

rules_iter = grammar.enumerate(25)
fns = list(set([rules_iter.next() for _ in xrange(20000)]))
fns = list(set(fns))
#hypotheses = list(set([MyHypothesis() for _ in xrange(10000)]))

hypotheses =[]
seen = set()
for f in fns:
	h = MyHypothesis()
	h.set_value(f)
	out = h()
	sn = h.value.count_nodes()
	if ((len(out) > 5 and ("1" in out and "0" in out))
		and (sn <= 4 or out[:15] not in seen)):
		hypotheses.append(copy.deepcopy(h))
		seen.add(out[:15])

	#print h
	#print h()
hypotheses = list(set(hypotheses))

stall = 5
stall_t = time.time()
for h in hypotheses:
	print h, h()

print len(hypotheses)
print time.time() - t_start

while time.time() - stall_t < stall:
	pass

hypotheses = run_hyps(hypotheses)

hypotheses = list(set(hypotheses))

for h in sorted(hypotheses):
	print h, h()
	print

print len(hypotheses)
print time.time() - t_start
##############################################################
###################GET RULES##################################

from LOTlib.GrammarInference.Precompute import create_counts

which_rules = [r for r in grammar if r.nt not in ['START']]

output_rules_helpers(which_rules, "grammar_inference/header.csv")



#for l1 in lsts:
	#for l2 in lsts:
#l1 = lsts[0]
#l2 = lsts[1]

for trntrans in ["train", "trans"]:

	for training in xrange(len(conditioned_on)):
		counts, sig2idx, prior_offset = create_counts(grammar, hypotheses,
							 which_rules=which_rules)


		##############################################################
		#####################GET HUMAN YN COUNTS######################



		#data_dct = get_training_data("data/outR.csv", str(trntrans))
		#data_dct = get_data_by_condition("data/outR.csv", 
					#l1, l2, str(trntrans))
		if trntrans == "train":
			data_dct = get_data_conditioned("data/outR.csv", 
						#conditioned_on[training],
						"all",
						  '0')
		else:
			data_dct = get_data_conditioned("data/outR.csv", 
				conditioned_on[training],  '1')

		#print data_dct.keys()
		N0 = []
		N1 = []
		conditions = []
		for d in data_dct:
			conditions.append(d)
			N0.append(data_dct[d][0])
			N1.append(data_dct[d][1])


		##############################################################
		#####################GET MOD YN PROB##########################

		if len(conditions) != 0:

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
			#file = "h5_files/data_all_%s.h5" % (["training", "transfer"][trntrans])
			file = "h5_files/%s_%s.h5" % (trntrans, conditioned_on[training])
			with h5py.File(file, 'w') as hf:
				# first write the 'specs'
				hf.create_dataset('specs',    data=[NHyp, sum(ntlen), len(N1), len(ntlen)], dtype=int)
				# write all the data
				hf.create_dataset('counts',    data=numpy.ravel(counts[:NHyp ], order='C'), dtype=int) # must be sure if we stop early, we don't include too many counts
				hf.create_dataset('output',    data=output, dtype=float)
				hf.create_dataset('human_yes', data=numpy.ravel(N1, order='C'), dtype=int)
				hf.create_dataset('human_no',  data=numpy.ravel(N0, order='C'), dtype=int)
				hf.create_dataset('likelihood',  data=numpy.ravel(L, order='C'), dtype=float)
				hf.create_dataset('ntlen', data=ntlen, dtype=int)
