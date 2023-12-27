from setuptools import setup, find_packages

setup(
    name='DataPrepKit2Ahmed',
    version='0.1',
    packages=find_packages(),
    description='Class to seamlessly read data from various file formats, provide a data summary, handle missing values, and encode categorical data.',
    author='Ahmed Esmail',
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn'
    ],
)