from setuptools import setup
from os import path

with open("README.md", "r") as ld:
    long_description = ld.read()

setup(
    name='txtd2c',
    version='0.0.1',
    description='Compares dictionary text file \
                to a plain text file with results in a CSV.',
    long_description=long_description,
    url='https://github.com/davidprush/txtd2c',
    author='David Rush',
    author_email='davidprush@gmail.com',
    license='MIT',
    packages=[],
    install_requires=['collections>=2.1.0',
                      'nltk>=3.7.0',
                      'fuzzywuzzy>=3.7.0',
                      'progressbar>=2.5.0',
                      'verboselogs>=1.7.0',
                      'pandas>=1.4.2'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Students/Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)