import timeit

# convenience variable for filling in new python scripts
header = '''import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import os
from jwpy.misc import Timer
from jwpy.explore_funcs import summarize_df

pd.set_option('display.max_columns', 250)
pd.set_option('display.max_rows', 250)

os.getcwd()
# os.chdir()'''


class Timer:
    '''
    Usage:
    with Timer():
        result = cool_stuff()

    Note that commands that in the with block will only print output if print()
    is explicitly called on the result

    Code ripped from:
    http://code.activestate.com/recipes/577896-benchmark-code-with-the-with-statement/
    '''
    def __init__(self, timer=None, disable_gc=False, verbose=True):
        if timer is None:
            timer = timeit.default_timer
        self.timer = timer
        self.disable_gc = disable_gc
        self.verbose = verbose
        self.start = self.end = self.interval = None
    def __enter__(self):
        if self.disable_gc:
            self.gc_state = gc.isenabled()
            gc.disable()
        self.start = self.timer()
        return self
    def __exit__(self, *args):
        self.end = self.timer()
        if self.disable_gc and self.gc_state:
            gc.enable()
        self.interval = self.end - self.start
        if self.verbose:
            print('time taken: %f seconds' % self.interval)
