import bs4
import names
import phonenumbers
import playwright
import requests
import setuptools
from setuptools import setup, find_packages

setup(
    name='automation_utilities',
    version='1.5.1',
    packages=find_packages(),
)

install_requires = [requests, setuptools, bs4, playwright, names, phonenumbers]
