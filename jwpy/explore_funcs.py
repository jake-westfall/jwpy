import numpy as np 
import pandas as pd 
import scipy as sp
import seaborn as sns
import matplotlib.pyplot as plt
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


def aov_xtab(endog, index, columns, figsize=(13, 8)):
	'''
	Exploratory plot for pairs of categorical predictors/features.
	Args:
		endog:
		index:
		columns:
		figsize:
	'''

	dat = pd.DataFrame({
	    'k': train.groupby(['source_screen_name','source_type'])['target'].sum(),
	    'n': train.groupby(['source_screen_name','source_type'])['target'].count()
	})
	a, b = betabinom(endog=dat).fit().params

	# compute the shrunken cell means and sort the matrix by row/column means
	shrunk = pd.pivot_table(train, values='target', index='source_screen_name',
	                        columns='source_type', aggfunc=shrink, fill_value=a/(a+b))
	new_index = shrunk.index[shrunk.mean(1).argsort()[::-1]]
	new_columns = shrunk.columns[shrunk.mean(0).argsort()[::-1]]
	shrunk = shrunk.reindex_axis(new_index, axis=0).reindex_axis(new_columns, axis=1)

	# compute the numbers of obs. per cell and sort by the same means as above
	annot = pd.crosstab(train['source_screen_name'], train['source_type'])
	annot = annot.reindex_axis(new_index, axis=0).reindex_axis(new_columns, axis=1)

	# print stuff
	print('SD of row means: {}'.format(shrunk.mean(1).std()))
	print('SD of column means: {}'.format(shrunk.mean(0).std()))
	interaction = shrunk.sub(shrunk.mean(1), axis=0).sub(shrunk.mean(0), axis=1)
	print('SD of row*column interaction: {}'.format(interaction.stack().std()))

	# plot!
	fig, ax = plt.subplots(figsize=figsize)
	return sns.heatmap(shrunk, annot=annot, fmt='.0f');

