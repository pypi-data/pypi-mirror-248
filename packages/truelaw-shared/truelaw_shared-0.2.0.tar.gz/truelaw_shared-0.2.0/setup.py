from setuptools import setup, find_packages

setup(
    name='truelaw_shared',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
       'openai'
    ],
)
