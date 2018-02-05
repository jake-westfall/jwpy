import numpy as np
import pandas as pd
import os
import re
from jwpy.explore_funcs import summarize_df
import pyhcup


def read_hcup(data_file, sas_script, chunksize=500000, combine_chunks=True,
              return_meta=False):
    '''
    Arguments:
        data_file (str): Path of fixed-width text data file
        sas_script (str): Path of the accompanying SAS load file
        chunksize (int): Break data_file into chunks with nrows=chunksize and
            read/process each chunk separately (for lower memory usage)
        combine_chunks (bool): Return single DataFrame with all chunks combined
            (True; default), or return list of DataFrame chunks (False)
        return_meta (bool): Return the data + a DataFrame of column metadata
            (True), or just return the processed data (False; default)

    Returns:
        Default: a single pandas DataFrame
        If combine_chunks=False: List of pandas DataFrames
        If return_meta=True: Tuple with data in first element and metadata in
            second element
    '''
    # read in the sas script
    with open(sas_script) as f:
        sas = f.readlines()

    # grab the lines that define the fields
    fields = [re.search(r'@\s*(\d+)\s+(\S+)\s+(\S+)\s?', x) for x in sas]
    fields = [x.groups() for x in fields if x]

    # from those, grab the names and starting positions, and infer the dtypes
    starts = [int(x[0]) for x in fields]
    names = [x[1] for x in fields]
    dtype = ['category' if re.search(r'CHAR', x[2]) else float for x in fields]
    # must use floats, since int columns can't have missing values
    # because it's okay because floats hardly use more space than ints

    # convert dtype list into dictionary (for pd.read_fwf)
    dtype = {name: dt for name, dt in zip(names, dtype)}

    # compute the variable widths
    maxcols = int(re.search(r'LRECL = (.+);', ''.join(sas)).group(1))
    widths = np.diff(starts + [maxcols+1])

    # grab all the missing value codes
    na_vals = re.findall(r'\'(.+)\' = \S+', ''.join(sas))
    na_vals += ['.']

    # read the data from disk in bite-sized chunks
    dat = pd.read_fwf(data_file, header=None, names=names, widths=widths,
                      dtype=dtype, na_values=na_vals, chunksize=chunksize)
    # convert generator to list
    dat = list(dat)

    if len(dat) > 1:
        # preserve categories instead of converting to objects.
        # if you concat categories w/ different levels (or even the same in a
        # different order), it silently converts to object
        levels = {col: set() for col in dtype.keys()}
        for col, dt in dtype.items():
            if dt == 'category':
                for d in dat:
                    levels[col] = set.union(levels[col], d[col].cat.categories)
                for d in dat:
                    _newlevels = list(levels[col] - set(d[col].cat.categories))
                    d[col] = d[col].cat.add_categories(_newlevels)
                    d[col] = d[col].cat.reorder_categories(levels[col])

    # recombine the chunks and return the result
    dat = pd.concat(dat)
    return dat
