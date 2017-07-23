from LOTlib.Primitives import primitive
from LOTlib.Miscellaneous import Infinity
from LOTlib.Grammar import Grammar
from collections import defaultdict
import numpy



##################################################################
####################HELPERS####################################


def hamming_distance(s1, s2):
    assert(len(s1) == len(s2))
    dif = 0
    for i in xrange(len(s1)):
        if s1[i] != s2[i]:
            dif += 1
    return dif


##################################################################
####################PRIMITIVES####################################

#GLOBAL MAX STRING LENGTH
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



###################################################################
######################GRAMMAR######################################

grammar = Grammar(start='TERM')

for i in xrange(0,5):
	grammar.add_rule('INT', str(i), None, 1.0) #
grammar.add_rule('INT', str(MAX), None, 1.0)


grammar.add_rule('TERM', "'0'", None, 1.0)
grammar.add_rule('TERM', "'1'", None, 1.0)
grammar.add_rule('TERM', 'repeat', ['TERM', 'INT'], 1.0)
grammar.add_rule('TERM', 'append', ['TERM', 'TERM'], 1.0) 

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
        datum = data[0].output
        datum_val = datum.keys()[0]
        length = datum[datum.keys()[0]]

        model_val = self.__call__()

        #near 0 probability mass for anything
        #less than length of already observed data...
        #...how could it have generated?
        # (...maybe not good for MCMC)
        if len(model_val) < length+1:
            return MAX * log(1.0 - alpha)

        else:
            hd = hamming_distance(datum_val, model_val[:length])
        return hd * log(1.0 - alpha) + (length - hd) * log(alpha)



if __name__ == "__main__":
    from LOTlib.SampleStream import *
    from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
    from LOTlib.DataAndObjects import FunctionData
    import time
    import copy

    seq = "0011001100"
    stps = 100000

    h0 = MyHypothesis()

    data = [FunctionData(alpha=1.0-10e-6, input=(),
        output={seq: len(seq)})]

    print "hmm"
    for h in SampleStream(MHSampler(h0, data, steps=stps)):

        r = h()
        print h
        print r
        print 