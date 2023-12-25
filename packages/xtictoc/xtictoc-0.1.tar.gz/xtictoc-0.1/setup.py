from setuptools import setup, find_packages

setup(
    name='xtictoc',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'xtictoc=xtictoc.__main__:main',
        ],
    },
)