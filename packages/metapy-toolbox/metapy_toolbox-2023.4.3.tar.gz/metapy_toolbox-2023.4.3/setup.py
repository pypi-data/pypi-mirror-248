from setuptools import setup

setup(
    	name = 'metapy_toolbox',
    	version = '2023.4.3',
		url = 'https://wmpjrufg.github.io/METAPY/',
    	license = 'MIT license',
    	author_email = 'wanderlei_junior@ufcat.edu.br',
    	packages = ['metapy_toolbox'],
    	description = "The METApy optimization toolbox is an easy-to-use environment for applying metaheuristic optimization methods. The platform has several optimization methods and functions for generating charts and statistical analysis of the results.",
    	classifiers = ["Programming Language :: Python","Topic :: Scientific/Engineering :: Mathematics", "Topic :: Scientific/Engineering"],
    	install_requires = ["numpy", "pandas"]
     )

# pip install setuptools
# python setup.py sdist
# pip install twine
# twine upload dist/*