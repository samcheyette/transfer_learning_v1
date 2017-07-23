import string
import copy
from analyze_sim_exp_data import *

#JUST A FILE TO CLEAN UP THE DATA...
#BORING STRING FORMATTING STUFF....

def convert(s):
	newX = ""

	for i in s:
		if "or" in i:
			newX += "a"
		else:
			newX += "b"
	return newX
				

def getGoodData(file):
	data = open(file, "r")
	l = data.readline()
	dataGood = {}
	people = {}
	while l != "":
		datum = l.rsplit(",")
		if ("debug" not in datum[0].lower() and 
				('bl' in datum[len(datum)-1] or 
					'or' in datum[len(datum)-1])):

			if datum[0] not in people:
				people[datum[0]] = []
			people[datum[0]].append(datum[4:])

		l = data.readline()
	data.close()
	conds = {}
	for p in people:
		if len(people[p]) >= 2:
			stim1 = convert(people[p][0][0].strip().rsplit("><"))
			stim2 = convert(people[p][1][0].strip().rsplit("><"))
			resp1 = convert(people[p][0][1].strip().rsplit("> <"))
			resp2 = convert(people[p][1][1].strip().rsplit("> <"))	

			if (stim1, stim2) not in conds:
				conds[(stim1, stim2)] = []
			conds[(stim1, stim2)].append((resp1, resp2))
		if len(people[p]) >= 4:

			stim1 = convert(people[p][2][0].strip().rsplit("><"))
			stim2 = convert(people[p][3][0].strip().rsplit("><"))
			resp1 = convert(people[p][2][1].strip().rsplit("> <"))
			resp2 = convert(people[p][3][1].strip().rsplit("> <"))	

			if (stim1, stim2) not in conds:
				conds[(stim1, stim2)] = []
			conds[(stim1, stim2)].append((resp1, resp2))



	return conds	

def output(data, conds, similarity, outfile, whichcare=2):
	out = "consistent, condition, timestep, subject, correct, which, prevexp, sim\n"

	out = "consistent, condition, timestep, subject, correct, which, prevexp, sim\n"

	subj = 0
	for k in data:
		s1 = k[0]
		s2 = k[1]


		if (s1, s2) in conds:
			cons = 1
		else:
			cons = 0

		for val in data[k]:

			r1 = val[0]
			r2 = val[1]
			for t in xrange(len(s1)):


				stm1 = s1[t]
				rsp1 = r1[t]
				stm2 = s2[t]
				rsp2 = r2[t]

				corr1 = (stm1 == rsp1) * 1
				corr2 = (stm2 == rsp2) * 1

				sim = 0.0
				if (s1, s2) in similarity:
					sim = (sum(similarity[(s1,s2)])/
								float(len(similarity[(s1,s2)])))

				else:
					sim = (sum(similarity[(s2,s1)])/
					float(len(similarity[(s2,s1)])))	

				if whichcare == 0 or whichcare == 2:
					out += "%d, %s, %d, %d, %d, %d, %s, %f\n" % (cons, s1, t, 
										subj, corr1, 0, s2, sim)
				
				if whichcare==1 or whichcare == 2:
					out += "%d, %s, %d, %d, %d, %d, %s, %f\n" % (cons, s2, t,
											subj, corr2, 1, s1, sim)

			subj += 1

	s_out = open(outfile, "w+")
	s_out.write(out)
	s_out.close()
	

if __name__ == "__main__":
	import random

	file = "data.csv"
	outfile = "outR_sim.csv"

	cleanData = getGoodData(file)
	for c in cleanData:
		print c, cleanData[c]

	sim_exp_data = get_clean_data("sim_exp.csv")
	lst_sim_data = []
	for d in sim_exp_data:
		lst_sim_data.append((d, sum(sim_exp_data[d])/float(len(sim_exp_data[d]))))
	lst_sim_data = sorted(lst_sim_data, key = lambda tup: -tup[1])

	for d in lst_sim_data:
		print d[0], d[1]

	gs = [('aabaabaabaabaab', 'aaabaaabaaabaaa'), 
			  ('baabaaabaaaabaa', 'abaabaaabaaaaba'),
			  ('aaaaaabbbbbbbbb', 'bbbbaaaaaaaaaaa'),
			  ('bbaaabbaaabbaaa', 'bbaaaabbaaaabba'),
			  ('bbbbbababababab', 'aaaabababababab'),
			  ('ababbababbababb', 'babaababaababaa')]

	new_gs = []
	which = 2
	for k in gs:
		#in experiment 2, 
		new_gs.append(k)
		new_gs.append((k[1], k[0]))


	s = 0
	for k in cleanData:
		s += len(cleanData[k])
	print s

	output(cleanData, new_gs, sim_exp_data,
				 outfile, whichcare=which)
	