import copy


def get_unigrams(conditions):
	unis = {}
	for cond in conditions:
		unis[cond] = []
		for x in xrange(len(cond[1])):
			so_far = cond[0] + cond[1][:x]
			p_b = so_far.count("b")/float(len(so_far))
			if cond[1][x] == "b":
				ac = 1.0
			else:
				ac = 0.0
			corr = 1.0 - abs(ac - p_b)
			unis[cond].append(corr)

	return unis


def occurrences(sub, string, sm=0.1):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count 


def get_bigrams(conds, unis):
	bigs = {}
	for cond in conds:
		bigs[cond] = []
		for x in xrange(len(cond[1])):
			so_far = cond[0] + cond[1][:x]
			last = so_far[-1]
			p_a = (occurrences("a", so_far))/float(len(so_far))
			p_b = (occurrences("b", so_far))/float(len(so_far))
			p_ba = occurrences("ba", so_far) 
			p_bb = occurrences("bb", so_far)
			p_ab = occurrences("ab", so_far) 
			p_aa = occurrences("aa", so_far) 

			norm= len(so_far) #(p_aa + p_ab + p_ba + p_b)

			if last == "a":
				p_ab /= float(norm)
				p_b_given_X = p_ab/(p_a)


			else:
				p_bb /= float(norm)
				p_b_given_X = p_bb/p_b


			if cond[1][x] == "b":
				ac = 1.0
			else:
				ac = 0.0
			#corr = p_b_given_X
			corr = 1.0 - abs(ac - p_b_given_X)
			bigs[cond].append(corr)

	return bigs


def get_bigrams(conds, unis):
	bigs = {}
	for cond in conds:
		bigs[cond] = []
		for x in xrange(len(cond[1])):
			so_far = cond[0] + cond[1][:x]
			last = so_far[-1]
			p_a = (occurrences("a", so_far))/float(len(so_far))
			p_b = (occurrences("b", so_far))/float(len(so_far))
			p_ba = occurrences("ba", so_far) 
			p_bb = occurrences("bb", so_far)
			p_ab = occurrences("ab", so_far) 
			p_aa = occurrences("aa", so_far) 

			norm= len(so_far) #(p_aa + p_ab + p_ba + p_b)

			if last == "a":
				p_ab /= float(norm)
				p_b_given_X = p_ab/(p_a)


			else:
				p_bb /= float(norm)
				p_b_given_X = p_bb/p_b


			if cond[1][x] == "b":
				ac = 1.0
			else:
				ac = 0.0
			#corr = p_b_given_X
			corr = 1.0 - abs(ac - p_b_given_X)
			bigs[cond].append(corr)

	return bigs

def get_human_data(file):
	f = open(file, "r")
	l = f.readline()
	l =f.readline()
	dct = {}
	counts = {}
	l1 =None
	while l != "":

		if "0" in copy.copy(l).split()[5]:
			l1 = copy.copy(l).split(",")

		if  ("1" in copy.copy(l).split(",")[5]):
			l2 = copy.copy(l).split(",")
			s1 = l1[1].replace(" ", "")
			s2 = l2[1].replace(" ", "")
			time = int(l2[2].replace(" ", ""))
			resp_corr = int(l2[4].replace(" ", ""))
			if (s1, s2) not in dct:
				dct[(s1,s2)] = [0.0 for _ in xrange(15)]
				counts[(s1, s2)] = 0.0
			dct[(s1,s2)][time] += resp_corr
			if time == 0:
				counts[(s1, s2)] += 1.0

		l = f.readline()

	norm_dct = {}
	for d in dct:
		norm_dct[d] = []
		for t in dct[d]:
			norm_dct[d].append(t/counts[(s1,s2)])
	f.close()
	return norm_dct


def output_unigram_human(human, model1, model2, cong, file):
	o = "training, transfer, is_congruent, time, who, corr\n"
	for h in human:
		s1 = h[0]
		s2 = h[1]
		h_resp = human[h]
		m_resp = model1[h]
		m2_resp = model2[h]

		if (s1, s2) in cong:
			congruent = "Congruent"
		else:
			congruent = "Incongruent"

		for t in xrange(len(h_resp)):
			o += ("%s, %s, %s, %d, Human, %f\n" % (s1, 
											s2, congruent,
											t, h_resp[t]))
			o += ("%s, %s, %s, %d, Unigram, %f\n" % (s1, 
											s2, congruent,
											t, m_resp[t]))
			o += ("%s, %s, %s, %d, Bigram, %f\n" % (s1, 
											s2, congruent,
											t, m2_resp[t]))
	f = open(file, "w+")
	f.write(o)
	f.close()
if __name__ == "__main__":

	seqs1 = ['aabaabaabaabaab','baabaaabaaaabaa','aaaaaabbbbbbbbb',
			'bbaaabbaaabbaaa', 'bbbbbababababab', 'ababbababbababb']
	seqs2 = ['aaabaaabaaabaaa','abaabaaabaaaaba', 'bbbbaaaaaaaaaaa',
			'bbaaaabbaaaabba','aaaabababababab','babaababaababaa']

	conditions = []

	for s1 in seqs1:
		for s2 in seqs2:
			conditions.append((s1, s2))

			conditions.append((s2, s1))

	unigrams = get_unigrams(conditions)
	# u in unigrams:
		#print u, unigrams[u]

	#print
	bigrams = get_bigrams(conditions, unigrams)

	hum_dat = get_human_data("outR.csv")
	for h in hum_dat:
		print h, hum_dat[h], bigrams[h]


	#for u in unigrams:
		#print u, unigrams[u]


	gs = [('aabaabaabaabaab', 'aaabaaabaaabaaa'), 
			  ('baabaaabaaaabaa', 'abaabaaabaaaaba'),
			  ('aaaaaabbbbbbbbb', 'bbbbaaaaaaaaaaa'),
			  ('bbaaabbaaabbaaa', 'bbaaaabbaaaabba'),
			  ('bbbbbababababab', 'aaaabababababab'),
			  ('ababbababbababb', 'babaababaababaa')]

	congruent = []
	for k in gs:
		congruent.append(k)
		congruent.append((k[1], k[0]))


	output_unigram_human(hum_dat, unigrams,bigrams,
				congruent, "comp_uni.csv")
