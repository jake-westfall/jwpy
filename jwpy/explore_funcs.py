import numpy as np 
import pandas as pd 
import scipy as sp
import seaborn as sns
import matplotlib.pyplot as plt
from functools import partial
from jwpy.betabinom import betabinom


def summarize_df(df, head=5, dropna=False):
    '''
    Quick summary of a pandas DataFrame.
    Args:
        df:
        head:
        dropna:
    '''
    
    # show variable types and numbers of unique levels
    summ = pd.DataFrame(
        [df.dtypes, df.nunique(dropna=dropna), df.isnull().mean(0)],
        index=['dtype','nunique','%missing'])
    # append head
    summ = pd.concat([summ, df.head(head)], axis=0)
    
    print('{} rows x {} columns'.format(*df.shape))
    return summ


def shrink(values, a, b):
    '''
    Apply empirical Bayes shrinkage to binomial counts for a given Beta prior.
    Args:
        values:
        a:
        b: 
    '''
    zeros, ones = ((values==0).sum(), (values==1).sum())
    return (a + ones)/(a + b + zeros + ones)


def aov_xtab(values, index, columns, figsize=(13, 8), **kwargs):
    '''
    Exploratory plot for pairs of categorical predictors/features.
    Args:
        values:
        index:
        columns:
        figsize:
        kwargs:
    '''

    # group the variables into a DataFrame
    dat = pd.DataFrame({
        'values': values,
        'index': index,
        'columns': columns
        })

    # fit the beta-binomial model
    endog = pd.DataFrame({
        'k': dat.groupby(['index','columns'])['values'].sum(),
        'n': dat.groupby(['index','columns'])['values'].count()
        })
    a, b = betabinom(endog=endog).fit(**kwargs).params
    m = a/(a+b)

    # compute the shrunken cell means and sort the matrix by row/column means
    shrunk = pd.pivot_table(dat, values='values', index='index',
        columns='columns', aggfunc=partial(shrink, a=a, b=b), fill_value=m)
    new_index = shrunk.index[shrunk.mean(1).argsort()[::-1]]
    new_columns = shrunk.columns[shrunk.mean(0).argsort()[::-1]]
    shrunk = shrunk.reindex_axis(new_index, axis=0)
    shrunk = shrunk.reindex_axis(new_columns, axis=1)

    # compute the numbers of obs. per cell and sort by the same means as above
    annot = pd.crosstab(dat['index'], dat['columns'])
    annot = annot.reindex_axis(new_index, axis=0)
    annot = annot.reindex_axis(new_columns, axis=1)

    # print stuff
    print('SD of row means: {}'.format(shrunk.mean(1).std()))
    print('SD of column means: {}'.format(shrunk.mean(0).std()))
    interaction = shrunk.sub(shrunk.mean(1), axis=0).sub(shrunk.mean(0), axis=1)
    print('SD of row*column interaction: {}'.format(interaction.stack().std()))

    # plot!
    fig, ax = plt.subplots(figsize=figsize)
    return sns.heatmap(shrunk, annot=annot, fmt='.0f');

