from setuptools import setup


setup(
    name='keycollator',
    version='0.1.0',
    py_modules=[
        'cli',
        'extractonator',
        'constants'
    ],
    install_requires=[
        'click',
        'progressbar',
        'verboselogs',
        'nltk',
        'fuzzywuzzy',
        'python-Levenshtein'
    ],
    entry_points='''
        [console_scripts]
        keycollator=keycollator:cli
    '''
)
