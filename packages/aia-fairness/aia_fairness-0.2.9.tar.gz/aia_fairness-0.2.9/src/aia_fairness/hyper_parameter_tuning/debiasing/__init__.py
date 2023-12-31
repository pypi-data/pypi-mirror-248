import pickle
import sys

if len(sys.argv)>1:
    if sys.argv[1]=="plot":
        print("plot mode")
        from .alpha_optimization import rule 
        from .. import config
        from .plot import *
        dsets = config.dsets
        attribs = config.attribs
        alphas = {}
        for dset in dsets:
            alphas[dset] = {}
            for attrib in attribs:
                alpha, fair, util, lim= rule(dset,attrib)
                alphas[dset][attrib] = alpha
                plot(dset,attrib)
                latex()
        with open("alpha.pickle", 'wb') as f:
            pickle.dump(alphas,f)

        quit()

print("run mode")
