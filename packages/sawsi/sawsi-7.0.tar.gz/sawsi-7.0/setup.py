from setuptools import setup, find_packages

setup(
    name="sawsi",
    version="7.0",
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0'
    ],
)
