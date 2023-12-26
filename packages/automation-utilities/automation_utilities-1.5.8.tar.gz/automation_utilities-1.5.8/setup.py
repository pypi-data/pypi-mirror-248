from setuptools import setup, find_packages

setup(
    name='automation_utilities',
    version='1.5.8',
    packages=find_packages(),
    install_requires=[
        'requests~=2.31.0',
        'setuptools~=65.5.1',
        'beautifulsoup4~=4.12.2',
        'playwright~=1.40.0',
        'names~=0.3.0',
        'phonenumbers~=8.13.27',
        'colorama~=0.4.6',
        'art~=6.1',
    ]
)
