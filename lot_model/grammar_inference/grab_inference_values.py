
from .. import Model



order = ["steps", "chain", "posterior", "alpha", "beta", "prior_temp", "ll_temp"]

which_rules = [r for r in grammar if r.nt not in ['START']]

for r in rules:
	sig = r.get_rule_signature()
	print sig

f = open("o.txt")
f.close()



