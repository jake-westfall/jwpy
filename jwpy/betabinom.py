import numpy as np 
import pandas as pd 
import scipy as sp
from statsmodels.base.model import GenericLikelihoodModel


class betabinom(GenericLikelihoodModel):
    '''
    Args:
        endog (2-column numpy array or pandas DataFrame): 1st column gives
            k (number of successes), 2nd column gives n (total number of trials).
        kwargs: Optional keyword arguments to pass onto GenericLikelihoodModel.
    '''

    def __init__(self, endog, **kwargs):
        super(betabinom, self).__init__(endog, extra_params_names=['a','b'], **kwargs)

    def pmf_log(self, endog, a, b):
        '''
        Log probability mass function (PMF) for beta-binomial distribution.
        Args:
            endog: see betabinom class docstring.
            a, b (float or array): parameters of underlying Beta distribution.
        '''
        if isinstance(endog, pd.core.frame.DataFrame):
            endog = endog.values
        k, n = endog.T
        
        result = \
            np.array([np.log(np.arange(i, 1, -1)).sum() for i in n]) \
            - np.array([np.log(np.arange(i, 1, -1)).sum() for i in k]) \
            - np.array([np.log(np.arange(i, 1, -1)).sum() for i in n-k]) \
            + sp.special.betaln(k+a, n-k+b) \
            - sp.special.betaln(a, b)
            
        return result
        
    def nloglikeobs(self, params):
        ''''Evaluates the negative log-likelihood.'''
        ll = self.pmf_log(self.endog, *params)
        return -ll.sum()
    
    def fit(self, start_params=np.array([2., 2.]), **kwargs):
        '''Estimates the model parameters.'''
        return super(betabinom, self).fit(start_params=start_params, **kwargs)

