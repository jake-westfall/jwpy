import timeit
import numpy as np
import pandas as pd

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
    Similar to the `%%time` magic, but it doesn't have to be run at the top of
    the cell, and the indentation makes it a little nicer visually. Usage:
    ```
    with Timer():
        result = cool_stuff()
    ```
    Note that commands in the with block will only print output if print() is
    explicitly called on the result

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


def align_cols(df1, df2):
    '''
    Wrapper for pandas.DataFrame.align(..., axis=1) to prepare dataframes for
    being stacked with pandas.concat(). Makes categoricals have the same
    categories so they won't be case to 'object' during stacking, and downcasts
    float64 types to float32 where possible to save memory.

    Args:
        df1, df1: The two dataframes to align column-wise, fill in missing
            columns/values, etc.

    Returns:
        A tuple containing (df1_aligned, df2_aligned).
    '''
    # align using pandas
    p1, p2 = df1.align(df2, axis=1)
    # define empty sets to hold the categories of each categorical
    levels = {col: set() for col in p1.columns}
    for col in levels.keys():
        # preserve categories
        check = str(p1[col].dtype) == 'category', str(p2[col].dtype) == 'category'
        if check[0] | check[1]:
            # make sure they're BOTH categoricals first
            if xor(check[0], check[1]):
                if check.index(True):
                    p1[col] = p1[col].astype('category')
                else:
                    p2[col] = p2[col].astype('category')
            # make sure both categoricals have the same categories
            for d in (p1, p2):
                levels[col] = set.union(levels[col], d[col].cat.categories)
            for d in (p1, p2):
                _newlevels = list(levels[col] - set(d[col].cat.categories))
                d[col] = d[col].cat.add_categories(_newlevels)
                d[col] = d[col].cat.reorder_categories(levels[col])
        # downcast float64 to float32
        else:
            for d in (p1, p2):
                if str(d[col].dtype) == 'float64':
                    d[col] = pd.to_numeric(d[col], downcast='float')
    return p1, p2
