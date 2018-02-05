====
# jwpy
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

* ``summarize_df()``: Quick summary of most important DataFrame info
* ``Timer``: Class for printing the execution time of expressions (use with ``with`` statement)
* ``header``: Constant for filling in top of new Python scripts
* ``aov_xtab()``: Exploratory function for examining crossing of two many-leveled factors
* ``betabinom``: Class implementing likelihood function for beta-binomial model; can be plugged into ``statsmodels``

Installation
------------

``pip install git+https://github.com/jake-westfall/jwpy.git``

Credits
---------

This package was created with Cookiecutter_ and the audreyr/cookiecutter-pypackage_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _audreyr/cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
