


def get_clean_data(file):
	f = open(file, "r")
	l = f.readline()
	dct = {}

	mapping = {"very_dissimilar":1, 
				"dissimilar": 2,
				"neither":3,
				"similar":4,
				"very_similar":5}
	c = 0
	while l != "":
		r = l.split(",")
		if len(r) > 5:
			s1 = r[3].replace(" ", "")
			s2 = r[4].replace(" ", "")
			rating = r[5].replace(" ", "").replace("\n","")
			if (((s1, s2) not in dct) and
				 ((s2, s1) not in dct)):
				dct[(s1,s2)] = []

			if (s1, s2) in dct:
				dct[(s1,s2)].append(mapping[rating])

			else:
				dct[(s2,s1)].append(mapping[rating])


		l = f.readline()

	return dct


if __name__ == "__main__":
	data = get_clean_data("sim_exp.csv")

	lst_data = []

	for d in data:
		lst_data.append((d, sum(data[d])/float(len(data[d]))))

	lst_data = sorted(lst_data, key = lambda tup: -tup[1])

	for d in lst_data:
		print d[0], d[1]