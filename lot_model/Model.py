from LOTlib.Primitives import primitive
from LOTlib.Miscellaneous import Infinity
from LOTlib.Grammar import Grammar
from helpers import *


##################################################################
####################PRIMITIVES####################################
INF=25
MAX = 20

@primitive
def append(s1, s2):
    if len(s1) >= MAX:
        return s1
    else:
        out = (s1 + s2)
        return out[:MAX]

@primitive
def repeat(x, n=MAX):
    out =""
    i = 0
    while len(out) < MAX and i < n:

        out += x
        i += 1


    return out[:MAX]


@primitive
def alternate_and_weave(s1, s2, x1, incr):
    ind = 0
    out = ""

    if incr + x1 == 0:
        return ""
    else:

        while ind < len(s1)  and len(out) < MAX:
            out += s1[ind:ind+x1]

            if len(out) < MAX:
                out += s2

            ind = ind + x1
            x1 = x1 + incr
           


        return out[:MAX]


@primitive
def weave(s1, s2):
    ind = 0
    out = ""
    while (ind < len(s1) and ind < len(s2)
                 and len(out) < MAX):
        out += s1[ind]
        out += s2[ind]
        ind += 1
    return out[:MAX]


@primitive
def increment(s1, s2, n):
    out = ""
    app = ""
    i=0
    while (i < n and len(out) < MAX):
        out += app
        out += s2
        app += s1
        i += 1
    return out[:MAX]


@primitive
def invert(x):
    inv = ""
    for i in x:
        if i == "0":
            inv += "1"
        else:
            inv += "0"
    return inv

@primitive
def alternate(s1, s2, n):
    out = ""
    i = 0
    while i < n  and len(out) < MAX:
        out += s1
        i += 1
        if i < n and len(out) < MAX:
            out += s2
        i += 1

    return out[:MAX]




@primitive
def from_n(x, n):
    if len(x) > n:
        return x[n:]
    else:
        return x

###################################################################
######################GRAMMAR######################################

grammar = Grammar(start='TERM')

for i in xrange(0,11):
	grammar.add_rule('INT', str(i), None, 1.0/(i+1.0)**2) #
grammar.add_rule('INT', str(INF), None, 1.0)


grammar.add_rule('TERM', "'0'", None, 5.0)
grammar.add_rule('TERM', "'1'", None, 5.0)
#grammar.add_rule('TERM', "'0'*25", None, 1.0)
#grammar.add_rule('TERM', "'1'*25", None, 1.0)

#grammar.add_rule('TERM', "repeat('0')", None, 2.0)
#grammar.add_rule('TERM', "repeat('1')", None, 2.0)
#grammar.add_rule('TERM', 'repeat', ['TERM'], 1.0)
grammar.add_rule('TERM', 'repeat', ['TERM', 'INT'], 1.0)

grammar.add_rule('TERM', 'append', ['TERM', 'TERM'], 0.25) 
grammar.add_rule('TERM', 'increment', ['TERM', 'TERM', 'INT'], 0.15) 

grammar.add_rule('TERM', 'weave', ['TERM', 'TERM'], 0.25) 
grammar.add_rule('TERM', 'invert', ['TERM'], 1.0) 
#grammar.add_rule('TERM', 'take_n', ['TERM', 'INT'], 0.5) 
grammar.add_rule('TERM', 'from_n', ['TERM', 'INT'], 1.0) 
grammar.add_rule('TERM', 'alternate', ['TERM', 'TERM', 'INT'], 0.25) 
#grammar.add_rule('TERM', 'alternate_and_weave', ['TERM', 'TERM', 'INT', 'INT'],
                                            #     1.0) 
######################################################################
######################################################################

from LOTlib.Miscellaneous import attrmem
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Hypotheses.Likelihoods.BinaryLikelihood import BinaryLikelihood

from LOTlib.Miscellaneous import Infinity, beta, attrmem
from LOTlib.FunctionNode import FunctionNode
from math import log, exp

class MyHypothesis(LOTHypothesis):
    def __init__(self, **kwargs):

        LOTHypothesis.__init__(self, grammar=grammar,
        maxnodes=400, display='lambda : %s', **kwargs)


    def __call__(self):
        out = LOTHypothesis.__call__(self)
        #if len(out) != MAX:
        #want to be able to generalize to N-lengthed sequences
        #sout = ""
        return out


    @attrmem('likelihood')
    def compute_likelihood(self, data, **kwargs):
        alpha = data[0].alpha

        try:
            require_n = data[0].require_n
        except:
            require_n=0

        datum = data[0].output
        datum_val = datum.keys()[0]
        length = datum[datum.keys()[0]]

        model_val = self.__call__()

        assert(require_n < MAX)
        if len(model_val) < require_n or len(model_val) < length+1:
            return INF * log(1.0 - alpha)

        else:
            hd = hamming_distance(datum_val, model_val[:length])
        return hd * log(1.0 - alpha) + (length - hd) * log(alpha)




if __name__ == "__main__":
    from LOTlib.SampleStream import *
    from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
    from LOTlib.DataAndObjects import FunctionData
    import time
    import copy
    lst = "00110011"
    stps = 100000
 
    h0 = MyHypothesis()
    data = [FunctionData(alpha=1.0-10e-6, input=(), output={lst: len(lst)})]

    #unit_tests()
    assert(False)
    stp = 0
    t1 = time.time()
    best = None
    best_posterior = None
    for h in SampleStream(MHSampler(h0, data, steps=stps)):

        r = h()
        if best_posterior == None or h.posterior_score >= best_posterior:
        	best = copy.deepcopy(h)
        	best_out = r
        	best_posterior = h.posterior_score

        if stp % 500 == 0:
        	print stp, float(stp+1)/(time.time() - t1)
        	try:
        		print hamming_distance(lst, r[:len(lst)])
        	except:
        		print len(lst)
	        print best
	        print best_out
	        print exp(best_posterior)
	        print
        stp=stp+1