
def get_transformations(file):
	f = open(file, "r+")
	l = f.readline()
	l = f.readline()

	dct = {}
	while l != "":
		r = l.split(",")

		s1 = r[0].replace(" ", "")
		s2 = r[1].replace(" ", "")
		n = int(r[2].replace(" ", ""))
		dct[(s1, s2)] = n
		l = f.readline()
	return dct

def get_rest(file, trns):
	f = open(file, "r+")
	o = "consistent,condition,timestep,ntrans,subject,correct,which,prevexp,sim\n"
	l = f.readline()
	l = f.readline()

	while l != "":
		r = l.split(",")
		s1 = r[1].replace(" ", "")
		s2 = r[6].replace(" ", "")
		ntrans=str(trns[(s1, s2)]) + ","
		#print s1, s2, trns[(s1, s2)]
		l = f.readline()
		new = ",".join(r[0:3]) + ","+ ntrans + ",".join(r[3:])
		o += new
	return o
if __name__ == "__main__":
	trans = get_transformations("transformations2.csv")
	other = get_rest("outR_sim.csv", trans)
	out = "outR_trans.csv"
	out = open(out, "w+")
	out.write(other)
	out.close()