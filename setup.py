"""
Insta485 python package configuration.

Andrew DeOrio <awdeorio@umich.edu>
"""

from setuptools import setup

setup(
    name='tonefinder',
    version='0.1.0',
    packages=['tonefinder'],
    include_package_data=True,
    install_requires=[
        'bs4==0.0.1',
        'Flask==1.0.2',
        'Flask-Testing==0.7.1',
        'requests==2.21.0',
        'sh==1.12.14',
        'mysqlclient==2.0.3'
    ],
)
