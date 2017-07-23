import re
import os
import string

def remove_line(inp):
	all_files = os.listdir(".")
	for f in all_files:
		if os.path.isfile(f) and re.match(inp, f) != None:

			old_f = open(f,"r")
			new_contents = ""
			remove_first = True
			while remove_first == True:
				l = old_f.readline()
				tmp = False
				for s in string.ascii_lowercase:
					if s in l:
						tmp = True
				if not tmp:
					remove_first = False


			while l != "":
				new_contents += l 
				l = old_f.readline()
			old_f.close()
			new_f = open(f, "w+")
			new_f.write(new_contents)
			new_f.close()

	return 1


if __name__ == "__main__":
	#inp = "tra.._.{15}.txt"
	inp = ".*?txt"
	remove_line(inp)

	#print re.match(x, pattern)
