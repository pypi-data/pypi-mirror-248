from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='bballRefWebScraper',
    version='0.1.0',
    description='A package that Grabs basketball data from basketball-reference',
    author='Michael Corbishley',
    author_email='corbishleymichael1@gmail.com',
    maintainer='Michael Corbishley',
    maintainer_email='corbishleymichael1@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/michaelc143/BballRefWebScraper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.6",

    # Package structure and location
    packages=find_packages(where='.', exclude=['tests']),

    install_requires=[
        'beautifulsoup4==4.12.2',
        'bs4==0.0.1',
        'lxml==4.9.3',
        'numpy==1.24.3',
        'pandas==2.0.3',
        'unidecode==1.2.0',
        'requests==2.31.0',
    ],
    extras_require={
        'test': ['pytest'],
    },

)