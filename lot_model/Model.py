from LOTlib.Primitives import primitive
from LOTlib.Miscellaneous import Infinity
from LOTlib.Grammar import Grammar
from collections import defaultdict
import numpy
from helpers import *


##################################################################
####################PRIMITIVES####################################
INF=35
MAX = 35

@primitive
def append(s1, s2):
    if len(s1) >= MAX:
        return s1
    else:
        out = (s1 + s2)
        return out[:MAX]

@primitive
def repeat(x):
    if len(x) >= MAX or len(x) < 1:
        return x
    else:
        out =""
        while len(out) < MAX:
            out += x

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

    if ind < len(s1) and len(out) < MAX:
        out += s1[ind:]
    elif ind < len(s2) and len(out) < MAX:
        out += s2[ind:]    
    return out[:MAX]



@primitive
def insert(s1, s2, n):
    if n == 0:
        return s1
    elif len(s1) == 0:
        return s2
    elif len(s2) == 0:
        return s1

    else:
        ind1 = 0
        out = ""
        while (ind1 < len(s1) and len(out) < MAX):
            if ind1 % n == 0:
                out += s2

            out += s1[ind1]
            ind1 += 1
        return out[:MAX]

@primitive
def delete(s, n):
    if n <= len(s):
        return s
    new_out = ""
    for i in xrange(len(s)):
        if i % n != 0:
            new_out += s[i]
    return new_out


@primitive
def replace(s1, s2, n):
    if n == 0:
        return s1
    ind1 = 0
    out = ""
    while (ind1 < len(s1) and len(out) < MAX):
        add = 1
        if ind1 % n == 0:
            out += s2
            add += 1
        out += s1[ind1]

        ind1 += add
    return out[:MAX]


@primitive
def increment(s1, s2, n):

    if len(s1) == 0:
        return s2
    elif len(s2) == 0:
        return s1
    else:
        out = ""
        app = ""
        while (len(out) < MAX):
            out += app
            out += s2
            app += min(1+MAX/len(s1), n) * s1
           # app += s1
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
def alternate(s1, s2):
    out = ""
    if len(s1) + len(s2) == 0:
        return ""

    else:
        while len(out) < MAX:
            out += s1
            if len(out) < MAX:
                out += s2

        return out[:MAX]



@primitive
def from_n(x, n):
    if len(x) > n:
        return x[n:]
    else:
        return ""

###################################################################
######################GRAMMAR######################################

grammar = Grammar(start='TERM')

for i in xrange(1,8):
	grammar.add_rule('INT', str(i), None, 1.0) #
grammar.add_rule('INT', str(INF), None, 5.0)


#grammar.add_rule('TERM1', "", None, 1e-10)
#grammar.add_rule('TERM', "%s", ['TERM1'], 1.0)
#grammar.add_rule('TERM1', "%s", ['TERM'], 0.1)

grammar.add_rule('TERM', "'0'", None, 1.0)
grammar.add_rule('TERM', "'1'", None, 1.0)
#grammar.add_rule('TERM', "'0'*35", None, 2.0)
#grammar.add_rule('TERM', "'1'*35", None, 2.0)
grammar.add_rule('TERM', 'append', ['TERM', 'TERM'], 0.25) 
grammar.add_rule('TERM', 'increment', ['TERM', 'TERM',
                                 'INT'], 0.125) 
grammar.add_rule('TERM', 'insert', ['TERM', 'TERM', 'INT'], 0.125) 
grammar.add_rule('TERM', 'from_n', ['TERM', 'INT'], 0.25) 
grammar.add_rule('TERM', 'alternate', ['TERM', 
                                         'TERM'], 0.125) 
grammar.add_rule('TERM', 'invert', ['TERM'], 0.25) 


#grammar.add_rule('TERM', "repeat('0')", None, 2.0)
#grammar.add_rule('TERM', "repeat('1')", None, 2.0)
#grammar.add_rule('TERM', 'repeat', ['TERM'], 0.25)
#grammar.add_rule('TERM', 'repeat', ['TERM', 'INT'], 0.5)
#grammar.add_rule('TERM', 'weave', ['TERM', 'TERM'], 0.125) 
#grammar.add_rule('TERM', 'delete', ['TERM', 'INT'], 0.25) 
#grammar.add_rule('TERM', 'replace', ['TERM', 'TERM', 'INT'], 0.25) 
#grammar.add_rule('TERM', 'take_n', ['TERM', 'INT'], 0.5) 

#grammar.add_rule('TERM', 'alternate_and_weave', ['TERM', 'TERM', 'INT', 'INT'],
                                            #     1.0) 

#####################################################################
def get_rule_counts(grammar, t, add_counts ={}):
    """
            A list of vectors of counts of how often each nonterminal is expanded each way

            TODO: This is probably not super fast since we use a hash over rule ids, but
                    it is simple!
    """

    counts = defaultdict(int) # a count for each hash type

    for x in t:
        if type(x) != FunctionNode:
            raise NotImplementedError("Rational rules not implemented for bound variables")
        
        counts[x.get_rule_signature()] += 1 


    for k in add_counts:
        counts[k] += add_counts[k]



    # and convert into a list of vectors (with the right zero counts)
    out = []
    for nt in grammar.rules.keys():
        v = numpy.array([ counts.get(r.get_rule_signature(),0) for r in grammar.rules[nt] ])
        out.append(v)
    return out


def RR_prior(grammar, t, alpha=1.0, add_counts={}):
    """
            Compute the rational rules prior from Goodman et al.

            NOTE: This has not yet been extensively debugged, so use with caution

            TODO: Add variable priors (different vectors, etc)
    """
    lp = 0.0

    for c in get_rule_counts(grammar, t, add_counts=add_counts):
        theprior = numpy.array( [alpha] * len(c), dtype=float )
        #theprior = np.repeat(alpha,len(c)) # Not implemented in numpypy
        lp += (beta(c+theprior) - beta(theprior))
    return lp


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

        self.start_counts = {}
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



    @attrmem('prior')
    def compute_prior(self,  rr_alpha=1.0):
        """
            Rational rules prior
        """
        if self.value.count_subnodes() > self.maxnodes:
            return -Infinity
        else:

            # compute the prior with either RR or not.
            return ((RR_prior(self.grammar, self.value,
                     alpha=rr_alpha,
                     add_counts=self.start_counts)) / 
                            self.prior_temperature)




if __name__ == "__main__":
    from LOTlib.SampleStream import *
    from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
    from LOTlib.DataAndObjects import FunctionData
    import time
    import copy
    lst = "00110011"
    stps = 100000

    #print weave_every('000000000', '1', 3)

    data = [FunctionData(alpha=1.0-10e-6, input=(), output={lst: len(lst)})]
    rules_iter = grammar.enumerate(10)

    start_counts = {}
    #for r in grammar:
       # if '0' in r.get_rule_signature()[1]:
         #   start_counts[r.get_rule_signature()] = 1


    s = 0
    for _ in xrange(50):
        h = rules_iter.next()
        h0 = MyHypothesis()
        h0.start_counts = start_counts
        #for h in grammar.get_rule
        #print h0.__dict__.get('rrAlpha', 1.0)

        h0.set_value(value=h)
        h0.compute_prior()
        h0.compute_likelihood(data)
        print s, h0.value, exp(h0.prior) #, h0.likelihood
        s += 1
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