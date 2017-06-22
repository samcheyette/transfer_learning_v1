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


def vanilla_conditions():
	stims = ["aabaabaabaabaab", "baabaaabaaaabaa", "aaaaaabbbbbbbbb", "bbaaabbaaabbaaa", "bbbbbababababab",
	             "ababbababbababb"]
	stims = [fromAB(s) for s in stims]
	endings = ["aaabaaabaaabaaa", "abaabaaabaaaaba", "bbbbaaaaaaaaaaa", "bbaaaabbaaaabba", "aaaabababababab",
	           "babaababaababaa"]
	endings = [fromAB(s) for s in endings]

	return stims+endings

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


def get_training_data(file):
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

		if which == '0':
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
