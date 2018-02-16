====
jwpy
====


.. image:: https://img.shields.io/pypi/v/jwpy.svg
        :target: https://pypi.python.org/pypi/jwpy

.. image:: https://img.shields.io/travis/jake-westfall/jwpy.svg
        :target: https://travis-ci.org/jake-westfall/jwpy

.. image:: https://readthedocs.org/projects/jwpy/badge/?version=latest
        :target: https://jwpy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/jake-westfall/jwpy/shield.svg
     :target: https://pyup.io/repos/github/jake-westfall/jwpy/
     :alt: Updates


Contains miscellaneous Python code useful to Jake Westfall (and maybe others).


* Free software: MIT license
* Documentation: https://jwpy.readthedocs.io.


Functions
--------

* ``explore_funcs`` module

  * ``summarize_df()``: Quick summary of most important DataFrame info
  * ``aov_xtab()``: Exploratory function for examining crossing of two many-leveled factors

* ``sas_fwf`` module

  * ``read_hcup()``: Reads in fixed-width text data files that are in the format used by HCUP
  * ``read_mhos()``: Reads in fixed-width text data files that are in the format used by MHOS
  * ``stack_chunks()``: Concatenate DataFrames without upcasting categoricals to objects

* ``betabinom`` module

  * ``betabinom``: Class implementing likelihood function for beta-binomial model; can be plugged into ``statsmodels``

* ``misc`` module

  * ``Timer``: Class for printing the execution time of expressions (use with ``with`` statement)
  * ``header``: Constant (string) useful for filling in top of new Python scripts
  * ``align_cols()``: Wrapper for pandas.DataFrame.align(..., axis=1) that prepares column dtypes for stacking
  * ``hcup_datadict()``: For quickly, easily building data dictionaries for HCUP datasets

Installation
------------

``pip install git+https://github.com/jake-westfall/jwpy.git``

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
