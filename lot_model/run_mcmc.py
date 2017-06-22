from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
from LOTlib.DataAndObjects import FunctionData
from LOTlib.TopN import TopN
from collections import Counter
from LOTlib.Miscellaneous import logsumexp, qq
from Model import *
import time
import copy


def run(lst, CHAINS, STEPS, TOPN, ALPHA, REQUIRE_N):

	h0 = MyHypothesis()
	data = [FunctionData(alpha=ALPHA, require_n=REQUIRE_N,
			input=(), output={lst: len(lst)})]

	chain = 0
	best_posterior = None
	t1 = time.time()

	tn = TopN(N=TOPN)
	while chain < CHAINS:
		stp = 0
		for h in MHSampler(h0, data, steps=STEPS):
			r = h()
			tn.add(h)
			if best_posterior == None or h.posterior_score > best_posterior:
				best = copy.deepcopy(h)
				best_out = r#[:30]
				best_posterior = h.posterior_score
				best_likelihood = h.likelihood
				best_prior= h.prior

			if stp % 500 == 0:
				print "*" * 50
				print "CHAIN    :", chain
				print "STEP     :", stp
				print "TIME/STEP:", float(chain * STEPS + stp+1)/(time.time() - t1)
				print "BEST HYP :", best
				print "DATA     :", lst
				print "BEST GEN :", best_out
				print "BEST POST:", exp(best_posterior)
				print "BEST LKLD:", exp(best_likelihood)
				print "BEST PRR :", exp(best_prior)

				print 
				print "RAND HYP :", h
				print "DATA     :", lst
				print "RAND GEN :", r#[:30]
				print "RAND POST:", exp(h.posterior_score)
				print "RAND LKLD:", exp(h.likelihood)
				print "RAND PRR :", exp(h.prior)

				print "*" * 50

				print

			stp=stp+1
		chain += 1


	z = logsumexp([h.posterior_score for h in tn])
	pp = [(h, exp(h.posterior_score - z)) for h in tn.get_all()]
	sort_post_probs = sorted(pp, key=lambda tup: 1 - tup[1])
	return sort_post_probs


def run_wrapper(data_dct):

	for training in data_dct.keys():
		hyps_out = run(training, CHAINS, STEPS, TOPN, ALPHA, REQUIRE_N)

		#for h in hyps_out:

		#for datum in data_dct[data]:
			#for lst in datum:
				#r = run(lst)

	



if __name__ == "__main__":
	CHAINS=3
	STEPS =10000

	TOPN=10
	ALPHA = 1.0-1.0e-4
	#how much generalization do we need?
	REQUIRE_N = 1


	data = experimental_conditions(True)
	data = collapse_lsts_to_dct(data)



	hyps_out = run("000010101010", CHAINS, STEPS, TOPN, ALPHA, REQUIRE_N)
	hyps_gen = get_hyp_gen(hyps_out)
	hyps_gen_probs = get_hyp_probs(hyps_gen, start=0, end=14)


	#for h in hyps_gen:
		#print h[0], h[1]


	#print [(float('%.2f' % x)) for x in hyps_gen_probs]
	#run_wrapper(data)




