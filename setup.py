from setuptools import setup, find_packages

import src
#from sys import path
#path.append('/usr/lib/pymodules/python2.7')

setup(
    name='Rocamgo',
    version=0.1,
    description='Rocamgo is recogniter of the go games by processing digital images with opencv',
    long_description='Rocamgo is recogniter of the go games by processing digital images with opencv extended',
    author='Victor Ramirez de la Corte',
    author_email='virako.9@gmail.com',
    url='https://github.com/virako/Rocamgo',
    download_url='https://github.com/virako/Rocamgo/downloads',
    license='GPLv3',
    packages=find_packages(exclude=['tests']),
    test_suite='tests',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Spanglish',
        'Operating System :: Linux',
        'Programming Language :: Python',
        ],
    )
