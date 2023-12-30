# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='KangRollGeneCancer',
    version='0.0.125',
    packages=find_packages(),
    package_data={
        'sa004package': [
            'kangroll_basic_fn001_mln_com_release.py',
            'pytransform/*',
            'pytransform/_pytransform.dylib'
        ],
        'sa005package': [
            'kangroll_basic_fn001_mln_com_release.py',
            'pytransform/*',
            'pytransform/_pytransform.dylib'
        ],
        'sa006package': [
            'kangroll_1vitarollplex_fn011_DynamicBoundaryAnchorSpectrum_release.py',
            'pytransform/*',
            'pytransform/_pytransform.dylib'
        ]
    },
    description='fn001 Python release edtion with KangTest',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='xiaowen',
    author_email='xiaowenseekjob@gmail.com',
    url='https://github.com/williampolicy/ToolkitKangRollGeneCancer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

