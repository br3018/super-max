from setuptools import setup, find_packages

setup(
    name='super-max',
    version='0.1.0',
    description='Repository for code to calcualte best F1 fantasy team based on historical data.',
    author='Benedict Rose',
    author_email='brbenrose@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'os',
        'itertools',
    ],
)