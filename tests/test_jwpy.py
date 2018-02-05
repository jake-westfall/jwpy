#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `jwpy` package."""

import pytest

from jwpy.explore_funcs import summarize_df
from jwpy.sas_fwf import head_hcup


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_read_hcup():
    files = ['NIS_2015_Core', 'NIS_2015_Hospital', 'NIS_2015Q1Q3_DX_PR_GRPS',
             'NIS_2015Q4_DX_PR_GRPS', 'NIS_2015Q1Q3_Severity',
             'NIS_2015Q4_Severity']
    datasets = [read_hcup(data_file='./fwf_test/'+f+'.fwf',
                          sas_script='./fwf_test/SASLoad_'+f+'.SAS',
                          chunksize=10) for f in files]
    summarize_df(datasets[4])
