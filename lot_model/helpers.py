import copy

def hamming_distance(s1, s2):
	assert(len(s1) == len(s2))
	dif = 0
	for i in xrange(len(s1)):
		if s1[i] != s2[i]:
			dif += 1

	return dif

def fromAB(s):
    #inverse of toAB
    ret = ""
    for j in s:
        if j == "a":
            l = "0"
        else:
            l = "1"
        ret += l
    return ret

def toAB(s):
    #inverse of toAB
    ret = ""
    for j in s:
        if j == "0":
            l = "a"
        else:
            l = "b"
        ret += l
    return ret



def experimental_conditions(returnBoth):
    stims = ["aabaabaabaabaab", "baabaaabaaaabaa", "aaaaaabbbbbbbbb", "bbaaabbaaabbaaa", "bbbbbababababab",
             "ababbababbababb"]
    stims = [fromAB(s) for s in stims]
    endings = ["aaabaaabaaabaaa", "abaabaaabaaaaba", "bbbbaaaaaaaaaaa", "bbaaaabbaaaabba", "aaaabababababab",
               "babaababaababaa"]
    endings = [fromAB(s) for s in endings]

    consistent = []
    inconsistent = []
    for i in xrange(len(stims)):
        for j in xrange(len(endings)):
            tmp = []
            for k in xrange(len(endings[j])):
                z = endings[j][:k+1]
                tmp.append(z)
            if i == j:
                consistent.append([stims[i]] + (copy.copy(tmp)))
  
            else:
                inconsistent.append([stims[i]] + (copy.copy(tmp)))
    stims = ["aaabaaabaaabaaa", "abaabaaabaaaaba", "bbbbaaaaaaaaaaa", "bbaaaabbaaaabba", "aaaabababababab",
               "babaababaababaa"]
    stims = [fromAB(s) for s in stims]   

    endings = ["aabaabaabaabaab", "baabaaabaaaabaa", "aaaaaabbbbbbbbb", "bbaaabbaaabbaaa", "bbbbbababababab",
             "ababbababbababb"]
    endings = [fromAB(s) for s in endings]
    for i in xrange(len(stims)):
        for j in xrange(len(endings)):
            tmp = []
            for k in xrange(len(endings[j])):
                z = endings[j][:k+1]
                tmp.append(z)
            if i == j:
                consistent.append([stims[i]] + (copy.copy(tmp)))
  
            else:
                inconsistent.append([stims[i]] + (copy.copy(tmp)))

    if returnBoth:
        return consistent + inconsistent
    else:
        return consistent


def vanilla_conditions(appstim=True, append=True):
	stims = []
	endings = []
	if appstim:
		stims = ["aabaabaabaabaab", "baabaaabaaaabaa", "aaaaaabbbbbbbbb", "bbaaabbaaabbaaa", "bbbbbababababab",
		             "ababbababbababb"]
		stims = [fromAB(s) for s in stims]
	if append:
		endings = ["aaabaaabaaabaaa", "abaabaaabaaaaba", "bbbbaaaaaaaaaaa", 
						"bbaaaabbaaaabba", "aaaabababababab",
		           "babaababaababaa"]
		endings = [fromAB(s) for s in endings]

	all_use = []
	for k in stims:
		all_use.append(k)
	for k in endings:
		all_use.append(k)

	return all_use

def collapse_lsts_to_dct(lsts):
	dct = {}
	for l in lsts:
		if l[0] not in dct:
			dct[l[0]] = []

		dct[l[0]].append(l[1:])
	return dct


def get_hyp_gen(hyps_out):
	dct = {}
	for h in hyps_out:
		prod = h[0]()
		prob = h[1]

		if prod not in dct:
			dct[prod] = 0.0
		dct[prod] += prob

	lst_hg = sorted([(k, dct[k]) for k in dct], key=lambda tup: 1 - tup[1])
	return lst_hg

def get_hyp_probs(hyps, start=0, end=14):
	assert(end > start)
	lst = [0.0 for _ in xrange(end - start + 1)]
	norm = [0.0 for _ in xrange(end - start + 1)]
	for hp in hyps:
		hyp = hp[0]
		prob = hp[1]
		for ind in xrange(end - start + 1):
			if len(hyp) > ind:
				norm[ind] += prob
				if hyp[ind] == '1':
					lst[ind] += prob


	ret = [0.0 for _ in xrange(end - start + 1)]
	for i in xrange(len(lst)):
		ret[i] = lst[i]/norm[i]


	return ret


def get_training_data(file, whichcare):
	f = open(file, "r")
	l = f.readline()
	l = f.readline()

	consistent = 0

	condition = 1
	timestep = 2
	subject = 3
	correct = 4
	train_or_transf = 5

	dct = {}
	while l != "":
		spl = ([x.replace("\n", "").replace(" ", "") 
					for x in l.split(",")])

		cons = spl[consistent]
		cond = spl[condition]
		time = spl[timestep]
		subj =spl[subject]
		corr = spl[correct]
		which = spl[train_or_transf]

		if which == whichcare:
			to_bin = fromAB(cond[:int(time)])
			resp = fromAB(cond[int(time)])
			if to_bin not in dct:
				dct[to_bin] = [0,0]

			if corr == '1':
				if resp == '0':
					dct[to_bin][0] += 1
				else:
					dct[to_bin][1] += 1
			else:
				if resp == '0':
					dct[to_bin][1] += 1
				else:
					dct[to_bin][0] += 1


		l =f.readline()	
	f.close()

	return dct



def get_data_by_condition(file, l1, l2, whichcare):
	f = open(file, "r")
	l = f.readline()
	l = f.readline()

	consistent = 0

	condition = 1
	timestep = 2
	subject = 3
	correct = 4
	train_or_transf = 5
	prev_experience = 6

	all_dcts = {}
	dct = {}
	while l != "":
		spl = ([x.replace("\n", "").replace(" ", "") 
					for x in l.split(",")])

		cons = spl[consistent]
		cond = fromAB(spl[condition])
		time = spl[timestep]
		subj =spl[subject]
		corr = spl[correct]
		which = spl[train_or_transf]
		prev = fromAB(spl[prev_experience])
		if ((which == whichcare and whichcare == '1'  
			and (prev == l1 and cond == l2))
			or (which == whichcare and whichcare == '0' 
				and cond == l1 and prev == l2)):
			to_bin_trn = cond[:int(time)]
			to_bin_exp = prev
			to_bin = (to_bin_exp, to_bin_trn)
			resp = cond[int(time)]
			if to_bin not in dct:
				dct[to_bin] = [0,0]


			if corr == '1':
				if resp == '0':
					dct[to_bin][0] += 1
				else:
					dct[to_bin][1] += 1
			else:
				if resp == '0':
					dct[to_bin][1] += 1
				else:
					dct[to_bin][0] += 1

		l =f.readline()	
	f.close()

	return dct



def get_data_conditioned(file, given_seq, whichcare):
	f = open(file, "r")
	l = f.readline()
	l = f.readline()

	consistent = 0

	condition = 1
	timestep = 2
	subject = 3
	correct = 4
	train_or_transf = 5
	prev_experience = 6

	all_dcts = {}
	dct = {}
	while l != "":
		spl = ([x.replace("\n", "").replace(" ", "") 
					for x in l.split(",")])

		cons = spl[consistent]
		cond = fromAB(spl[condition])
		time = spl[timestep]
		subj =spl[subject]
		corr = spl[correct]
		which = spl[train_or_transf]
		prev = fromAB(spl[prev_experience])
		if ((whichcare == '1' and which == '1' and prev == given_seq) or
			(whichcare == '0' and which == '0' and cond == given_seq)):
			


			to_bin = cond[:int(time)]
			resp = cond[int(time)]

			if to_bin not in dct:
				dct[to_bin] = [0,0]

			if corr == '1':
				if resp == '0':
					dct[to_bin][0] += 1
				else:
					dct[to_bin][1] += 1
			else:
				if resp == '0':
					dct[to_bin][1] += 1
				else:
					dct[to_bin][0] += 1

		l =f.readline()	
	f.close()

	return dct



def output_rules_helpers(rules, out_file):
	o = "steps, chain, posterior, proposal, alpha, beta, prior_temp, ll_temp"

	for r in rules:
		sig = r.get_rule_signature()
		print sig
		o += ","+sig[0] + "_" +sig[1].replace("'", "").replace(',',"")

	f = open(out_file, "w+")
	f.write(o)
	f.close()



if __name__ == "__main__":
	#x = get_data_by_condition("data/outR.csv", 
					#	"010110101101011", "101001010010100",
						# whichcare='1')
	#x = get_data_by_condition("data/outR.csv", 
			#			"101001010010100", "010110101101011",
					#	 whichcare='0')
	#x = get_data_by_condition("data/outR.csv", 
					#	"010010001000010", "100100010000100",
					#	whichcare ='0')
	#x = get_data_by_condition("data/outR.csv", 
						#"100100010000100", "010010001000010",
						#whichcare ='1')

	#x = get_data_by_condition("data/outR.csv", 
				#		"000000111111111", "111100000000000",
					#	whichcare ='0')

	x1 = get_data_conditioned("data/outR.csv", 
						"000000111111111",
						whichcare ='1')

	x2 = get_data_conditioned("data/outR.csv", 
						"001001001001001",
						whichcare ='1')
	#x = get_data_by_condition("data/outR.csv", 
						#"111100000000000", "000000111111111",
						#whichcare ='1')
	#print x
	#x2 = get_training_data("data/outR.csv", whichcare='1')
	
	print len(x1.keys())
	print len(x2.keys())
	for i in sorted(copy.deepcopy(x1.keys()), key=lambda tup: len(tup)):
		if i in x1 and i in x2:
			print i, x1[i][1]/float(x1[i][0] + x1[i][1]), x2[i][1]/float(x2[i][0] + x2[i][1])


