from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up

setup(
    # the name must match the folder name 'verysimplemodule'
    name = 'verysimplemodule_alisonVitorH',
    version = VERSION,
    author = 'Alison',
    author_email = 'alissonmarqueshm30@gmail.com',
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [],
    #add any additional packages that
    #needs to be installed along with your package. Eg 'caer'

    keywords = [],
    classifiers = []
    )
