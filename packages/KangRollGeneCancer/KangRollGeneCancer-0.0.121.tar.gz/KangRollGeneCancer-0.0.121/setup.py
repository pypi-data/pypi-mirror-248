# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='KangRollGeneCancer',
    version='0.0.121',
    packages=find_packages(),
    package_data={
        'sa005package': [
        # 'kangroll_basic_fn001_mln',
        'kangroll_basic_fn001_mln_release.py',
        'pytransform/*',
        'pytransform/_pytransform.dylib',
        'pytransform/_pytransform.dylib'],
    },
    description='fn001 Python release edtion with KangTest',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='xiaowen',
    author_email='xiaowenseekjob@gmail.com',
    url='https://github.com/yourusername/standalone001pyarmor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

