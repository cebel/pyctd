#!/usr/bin/env python
from setuptools import setup, find_packages

PACKAGES = find_packages(where='src')

INSTALL_REQUIRES = [
    'sqlalchemy', 'pandas'
]

ENTRY_POINTS = {
    'console_scripts': [
        'pybel = pybel.cli:main',
    ]
}

# entry_points=ENTRY_POINTS,
setup(
    name="pyctd",
    version='0.0.2',
    url='https://github.com/cebel/pyctd/',
    author='Christian Ebeling',
    author_email='chr.ebeling@gmail.com',
    maintainer='Christian Ebeling',
    maintainer_email='chr.ebeling@gmail.com',
    description='python lib for CTD',
    license="Apache 2.0",
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
    ],
)
