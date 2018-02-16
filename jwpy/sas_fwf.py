import numpy as np
import pandas as pd
import re


def stack_chunks(dat_list):
    '''
    For preserving categories instead of converting to objects.
    If you concat categories w/ different levels (or even the same in a
    different order), it silently converts to object
    '''
    columns, dtypes = dat_list[0].columns, dat_list[0].dtypes
    # preserve categories
    levels = {col: set() for col in columns}
    for col, dt in zip(columns, dtypes):
        if str(dt) == 'category':
            for d in dat_list:
                levels[col] = set.union(levels[col], d[col].cat.categories)
            for d in dat_list:
                _newlevels = list(levels[col] - set(d[col].cat.categories))
                d[col] = d[col].cat.add_categories(_newlevels)
                d[col] = d[col].cat.reorder_categories(levels[col])
    # recombine the chunks and return the result
    return pd.concat(dat_list)


def read_hcup(data_file, sas_script, chunksize=500000, combine_chunks=True,
              return_meta=False, strings_to_categorical=True, **kwargs):
    '''
    Arguments:
        data_file (str): Path of fixed-width text data file
        sas_script (str): Path of the accompanying SAS load file
        chunksize (int, default 500K): Break data into chunks of size chunksize
            and read/process each chunk separately (for lower memory usage)
        combine_chunks (bool, default True): Return single DataFrame with all
            chunks combined (True), or return list of DataFrame chunks (False)
        return_meta (bool, default False): Return the data + a DataFrame of
            column metadata (True), or just return the processed data (False)
        strings_to_categorical (bool, default True): Convert variables defined
            as CHAR in SAS script to pd.Categorical upon import
        kwargs: passed on to pandas.read_fwf()

    Returns:
        Default: a single pandas DataFrame
        If combine_chunks=False: Generator of pandas DataFrames
        If return_meta=True: Return metadata (widths, dtypes, etc. ) *instead
            of* the data
    '''
    # what dtype to use for text columns
    text = 'category' if strings_to_categorical else 'object'

    # read in the sas script
    with open(sas_script) as f:
        sas = f.readlines()

    # grab the lines that define the fields. returns three match groups:
    # 0 = starting position, 1 = field name, 2 = variable type
    fields = [re.search(r'@\s*(\d+)\s+(\S+)\s+(\S+)\s?', x) for x in sas]
    fields = [x.groups() for x in fields if x]

    # from those, grab the names and starting positions, and infer the dtypes
    starts = [int(x[0]) for x in fields]
    names = [x[1] for x in fields]

    # use different dtypes based on whether user requests metadata or data.
    # in the latter case we just make everything a category for max compression
    # for numerics, must use floats since int columns can't have missing values
    # but it's okay because floats hardly use more space than ints
    if return_meta:
        dtype = [text if re.search(r'CHAR', x[2]) else float for x in fields]
    else:
        # keep KEY_NIS as numeric so it can be safely sorted on
        dtype = [text if col != 'KEY_NIS' else float for col in names]

    # convert dtype list into dictionary (for pd.read_fwf)
    dtypes = dict(zip(names, dtypes))

    # compute the variable widths
    maxcols = int(re.search(r'LRECL = (.+);', ''.join(sas)).group(1))
    widths = np.diff(starts + [maxcols+1])

    # grab all the missing value codes
    na_vals = re.findall(r'\'(.+)\' = \S+', ''.join(sas))
    na_vals += ['.']

    # return meta-data if requested
    if return_meta:
        return {'names': names, 'starts': starts, 'widths': widths,
                'dtypes': dtype, 'na_values': na_vals}

    # get a generator that reads the data in chunks
    dat = pd.read_fwf(data_file, header=None, names=names, widths=widths,
                      dtype=dtype, na_values=na_vals, chunksize=chunksize,
                      **kwargs)

    # return generator if requested
    if not combine_chunks:
        return dat

    # convert generator to list and stack the dataframes if applicable
    dat = list(dat)
    if len(dat) > 1:
        dat = stack_chunks(dat)
    else:
        dat = dat[0]

    return dat


def read_mhos(sas_script, data_file=None, chunksize=500000, combine_chunks=True,
              return_meta=False, strings_to_categorical=True, **kwargs):
    '''
    Arguments:
        data_file (str): Path of fixed-width text data file
        sas_script (str): Path of the accompanying SAS load file
        chunksize (int, default 500K): Break data into chunks of size chunksize
            and read/process each chunk separately (for lower memory usage)
        combine_chunks (bool, default True): Return single DataFrame with all
            chunks combined (True), or return list of DataFrame chunks (False)
        return_meta (bool, default False): Return the data + a DataFrame of
            column metadata (True), or just return the processed data (False)
        strings_to_categorical (bool, default True): Convert variables defined
            as CHAR in SAS script to pd.Categorical upon import
        kwargs: passed on to pandas.read_fwf()

    Returns:
        Default: a single pandas DataFrame
        If combine_chunks=False: Generator of pandas DataFrames
        If return_meta=True: Return metadata (colspecs, dtypes, etc. ) *instead
            of* the data
    '''
    if data_file is None:
        return_meta = True

    # what dtype to use for text columns
    text = 'category' if strings_to_categorical else 'object'

    # read in the sas script
    with open(sas_script) as f:
        sas = f.readlines()

    # match groups (indexed from 1, not 0)
    # 1 = prefix, 2 = field name, 3 = string, 4 = start position,
    # 5 = end position, 6 = field number, 7 = field description
    regex = r'^\s+(&[c|C].|&[r|R].|&[p|P].)?(\S+)\s+(\$)?\s*(\d{1,3})-?(\d{1,3})?\S*\s*/\*\s+(\d{1,3})(.*)\*/'
    fields = [re.search(regex, x) for x in sas if re.search(regex, x)]

    # check that we matched all and only the the right field numbers
    assert [int(x.group(6)) for x in fields if x] \
        == list(range(1, len(fields)+1))

    # extract the meta-data
    prefix = [x.group(1) for x in fields]
    names = [x.group(2).lower() for x in fields]
    dtypes = [str if x.group(2)=='CASE_ID' else text if x.group(3) else float
              for x in fields]
    starts = [int(x.group(4))-1 for x in fields]
    ends = [int(x.group(5)) if x.group(5) else int(x.group(4)) for x in fields]
    descriptions = [x.group(7).strip() for x in fields]

    # handle duplicate names
    vc = pd.Series(names).value_counts()
    dupes = list(vc.index[vc > 1])
    dupes = [x in dupes for x in names]
    names = [prefix+name if dupe else name
             for prefix, name, dupe in zip(prefix, names, dupes)]

    # convert dtype list into dictionary (for pd.read_fwf)
    dtypes = dict(zip(names, dtypes))

    # return meta-data if requested
    if return_meta:
        return {'names': names, 'starts': starts, 'ends': ends,
                'dtypes': dtypes, 'descriptions': descriptions}

    # get a generator that reads the data in chunks
    dat = pd.read_fwf(data_file, header=None, names=names,
                      colspecs=list(zip(starts, ends)), dtype=dtypes,
                      chunksize=chunksize, **kwargs)

    # return generator if requested
    if not combine_chunks:
        return dat

    # convert generator to list and stack the dataframes if applicable
    dat = list(dat)
    if len(dat) > 1:
        dat = stack_chunks(dat)
    else:
        dat = dat[0]

    return dat
