from run_mcmc import *
import os.path

def resp_from_hyps(hps, l):
	prob = 0.0
	norm = 0.0
	for hp in hps:
		h = hp[0]
		p = hp[1]
		out = h()

		if len(out) >= len(l):
			norm += p
			if out[len(l)-1] == l[-1]:
				prob += p

	if norm == 0.0:
		return 0.0

	return prob/norm



def run_wrapper(training, transfer,which, add_counts={}):
	#global grammar
	orig_grammar = copy.deepcopy(grammar)

	#rational rules to-add counts (alpha=1.0 uniformly at first)
	#grammar=copy.deepcopy(orig_grammar)

	ret_dct = {}

	#print transfer

	if which == "rrules" or which == "both":
		hyps_out = run(training, CHAINS, STEPS*2, TOPN, 
			ALPHA, REQUIRE_N, add_counts, PRIOR_TEMP)
		for hp in hyps_out:
			cplx = len(hp[0].value)
			for x in hp[0].value:

				if x.get_rule_signature() not in add_counts:
					add_counts[x.get_rule_signature()] = 0
				add_counts[x.get_rule_signature()] += 4.0* hp[1]/float(cplx)
			print hp

		print "x*" * 50

		print
		for c in add_counts:
			print c, add_counts[c]
		print "x*" * 50



	if which == "reuse" or which == "both":
		add_g = "'%s'" % training
		grammar.add_rule("TERM", add_g, None, 0.5)
		grammar.renormalize()
		#add_counts[("TERM", add_g)] = 1



	for transf in transfer:

		seq = transf[len(transf)-1]
		ret_dct[seq] = [0.5]
		x = 0
		for l in transf[:len(transf)-1]:
			#print l
			hyps_out = run(l, CHAINS, STEPS, TOPN, 
				ALPHA, REQUIRE_N, add_counts, PRIOR_TEMP)
			print training, l
			for hp in hyps_out:
				print hp[0], hp[1], hp[0]()

			print 
			corr = resp_from_hyps(hyps_out, transf[x+1])
			print corr
			print "*" * 50
			x += 1

			ret_dct[seq].append(corr)

	return ret_dct


def output_by_inf(file, corr, which, training):
	dir_f = "original_model_out/" + file
	if (not os.path.isfile(dir_f)):
		out = "model_type, training, sequence, timestep, corr\n"
		f = open(dir_f, "w+")
	else:
		out = ""
		f =open(dir_f, "a+")

	for h in corr:
		for t in xrange(len(corr[h])):
			out += "%s, %s, %s, %d, %f\n" % (which, toAB(training), toAB(h),t, corr[h][t])


	f.write(out)
	f.close()




if __name__ == "__main__":
	import sys

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
	PRIOR_TEMP = float(sys.argv[counter()])

	ALPHA = float(sys.argv[counter()])
	REQUIRE_N = int(sys.argv[counter()])
	which = str(sys.argv[counter()])
	out_f = str(sys.argv[counter()])

	training = str(sys.argv[counter()])

	all_d = experimental_conditions(True)
	all_d = collapse_lsts_to_dct(all_d)
	for d in all_d.keys():
		if d == training:
			transfer = copy.deepcopy(all_d[d])


	add = {}
	#add = {("TERM", "'0'"):2.0, ("TERM", "'1'"):2.0}
			#("TERM", "increment", 'TERM', 'TERM', 'INT', 'INT'):-0.5,
				# ("TERM", "WEAVE", 'TERM', 'TERM'):-0.5}

	corr_seqs = run_wrapper(training, transfer, which, add)

	if which == 'none':
		if training in vanilla_conditions(appstim=True, append=False):
			for x in vanilla_conditions(appstim=True, append=False):
				output_by_inf(out_f, corr_seqs, which, x)

		else:
			for x in vanilla_conditions(appstim=False, append=True):
				output_by_inf(out_f, corr_seqs, which, x)			

	else:		

		output_by_inf(out_f, corr_seqs, which, training)

	for h in corr_seqs:
		print h, corr_seqs[h]

	#data = {training:collapse_lsts_to_dct[training]}