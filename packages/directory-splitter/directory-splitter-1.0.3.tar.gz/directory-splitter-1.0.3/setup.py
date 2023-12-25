from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='directory-splitter',
    version='1.0.3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'argparse',
       
    ],
    entry_points={
        'console_scripts': [
            'directory-splitter = tester.tester1:print_url',
        ],
    },
    
    description='A script to split and extract unique endpoints from a list of URLs.',
    license='MIT',
    keywords='directory-splitter url-parser',
    
)
