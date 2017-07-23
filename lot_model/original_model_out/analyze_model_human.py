from math import log, exp


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


def get_congruous():
	stims = ["aabaabaabaabaab", "baabaaabaaaabaa", "aaaaaabbbbbbbbb", "bbaaabbaaabbaaa", "bbbbbababababab",
			             "ababbababbababb"]
	ends = ["aaabaaabaaabaaa", "abaabaaabaaaaba", "bbbbaaaaaaaaaaa", 
							"bbaaaabbaaaabba", "aaaabababababab",
			           "babaababaababaa"]
	congruous = [(fromAB(stims[t]), fromAB(ends[t])) for t in xrange(len(stims))]
	congruous += [(fromAB(ends[t]), fromAB(stims[t])) for t in xrange(len(stims))]
	return congruous



def get_model_data(file):
	f = open(file, "r")
	l = f.readline()
	l = f.readline()
	ret_dct = {}
	while l != "":

		
		r = l.split(",")
		mod =r[0].replace(" ", "").replace("\n","")
		train = r[1].replace(" ", "").replace("\n","")
		seq = r[2].replace(" ", "").replace("\n","")
 		time = int(r[3].replace(" ", "").replace("\n",""))
 		corr = float(r[4].replace(" ", "").replace("\n",""))

 		ret_dct[(mod,train,seq,time)] = corr

		l =f.readline()


	return ret_dct

def get_human_data(file):
	f = open(file, "r")
	ret_dct = {}
	l=f.readline()
	l=f.readline()

	while l != "":

		r = l.split(",")
		cong = r[0].replace(" ", "").replace("\n","")
		transf = r[1].replace(" ", "").replace("\n","")
		time = int(r[2].replace(" ", "").replace("\n",""))
		subj = int(r[3].replace(" ", "").replace("\n",""))
		corr = int(r[4].replace(" ", "").replace("\n",""))
		which = r[5].replace(" ", "").replace("\n","")
		train = r[6].replace(" ", "").replace("\n","")

		if which == '1':
 			if (train, transf, time) not in ret_dct:
				ret_dct[(train, transf, time)] = []
			ret_dct[(train, transf, time)].append(corr)

		l =f.readline()

	return ret_dct


def p_mod_given_data(hum, mod, whichmod, sm=1.0e-4):
	logp = 0.0
	p = 1.0
	for k in mod:
		if k[0] == whichmod:
			pmod = mod[k]
			nhum = sum(hum_dat[(k[1], k[2],k[3])])
			ntot_hum =  len(hum_dat[(k[1], k[2],k[3])])
			p *= (pmod ** nhum) * ((1.0 - pmod) ** (ntot_hum - nhum))
			logp += (nhum * log(min(1.0, pmod + sm)) +
					 (ntot_hum - nhum) * log(min(1.0 - pmod + sm, 1.0)))


	return logp


def p_mod_for_each(hum, mod, sm=1.0e-4):
	logps = {}
	for k in mod:

		pmod = mod[k]
		nhum = sum(hum_dat[(k[1], k[2],k[3])])
		ntot_hum =  len(hum_dat[(k[1], k[2],k[3])])
		#p *= (pmod ** nhum) * ((1.0 - pmod) ** (ntot_hum - nhum))
		logp = (nhum * log(min(1.0, pmod + sm)) +
				 (ntot_hum - nhum) * log(min(1.0 - pmod + sm, 1.0)))

		newk= (k[1], k[2])
		if newk not in logps:
			logps[newk] = {}

		if k[0] not in logps[newk]:
			logps[newk][k[0]] = 0.0



		logps[newk][k[0]] += logp

	return logps



def output_for_r(mod, hum, out_f):
	out = "model_human, training, transfer, congruous, timestep, pcorr, LL\n"

	seen = set()
	cong_pairs = get_congruous()
	for k in mod:
		pmod = mod[k]
		if (fromAB(k[1]), fromAB(k[2])) in cong_pairs:
			cong = 1
		else:
			cong = 0

		sm = 1e-4
		nhum = sum(hum_dat[(k[1], k[2],k[3])])
		ntot_hum =  len(hum_dat[(k[1], k[2],k[3])])
		logp = (nhum * log(min(1.0, pmod + sm)) +
					 (ntot_hum - nhum) * log(min(1.0 - pmod + sm, 1.0)))
		
		out += ("%s, %s, %s, %d, %d, %f, %f\n" % (k[0], k[1],
											 k[2], cong, k[3], 
											 pmod, logp))

		if (k[1], k[2],k[3]) not in seen:
			phum = nhum/float(ntot_hum)

			out += "%s, %s, %s, %d, %d, %f, 0.0\n" % ("hum", k[1], k[2], 
								cong, k[3], phum)
			
			seen.add((k[1], k[2],k[3]))

	f = open(out_f, "w+")
	f.write(out)
	f.close()


if __name__ == "__main__":
	mod_dat = get_model_data("out3.csv")
	hum_dat = get_human_data("out_human.csv")
	cong = get_congruous()

	(rule, norm_rule, reuse, 
		norm_reuse, none,norm_none, 
		hum, norm_hum, bot, norm_bot) = (0.0, 
							0.0,0.0,0.0, 0.0, 0.0,
								 0.0,0.0, 0.0, 0.0)

	for k in mod_dat:
		if (fromAB(k[1]), fromAB(k[2])) not in cong:
			if k[0] == "rrules":
				rule += mod_dat[k]
				norm_rule += 1
			elif k[0] == "reuse":
				reuse += mod_dat[k]
				norm_reuse += 1
			elif k[0] == "none":
				none += mod_dat[k]
				norm_none += 1
			else:
				bot += mod_dat[k]
				norm_bot += 1
			hum += sum(hum_dat[(k[1], k[2],k[3])])
			norm_hum += len(hum_dat[(k[1], k[2],k[3])])


	print (hum/float(norm_hum), rule/float(norm_rule),
				reuse/float(norm_reuse), 
				none/float(norm_none),
				bot/float(norm_bot))

	prrules = p_mod_given_data(hum_dat, mod_dat, "rrules")
	preuse = p_mod_given_data(hum_dat, mod_dat, "reuse")
	pnone = p_mod_given_data(hum_dat, mod_dat, "none")
	pboth = p_mod_given_data(hum_dat, mod_dat, "both")

	peach = p_mod_for_each(hum_dat, mod_dat)

	s = 0.0
	counts = {}
	for k in peach:
		best = ""
		whch = ""

		if (fromAB(k[0]), fromAB(k[1])) in cong:
			whch = "Congruous"
		else:
			whch = "Incongruous"

		best_p = None
		for b in peach[k]:
			if (b,whch) not in counts:
				counts[(b, whch)] = 0
			if best_p == None or peach[k][b] > best_p:
				best_p = peach[k][b]
				best = b
		counts[(best, whch)] += 1

	print counts




	z = [x[0] for x in mod_dat.keys()]
	print z.count("none"), z.count("rrules"), z.count("reuse"), z.count("both")
	print [-2 * x for x in [pnone, prrules, preuse, pboth]]

	output_for_r(mod_dat, hum_dat, "r_analysis.csv")