from setuptools import setup, find_packages

setup(
    name='custom-xorbits-dg',
    version='0.1.2',
    author='antonvls',
    description='A custom version of xorbits library',
    packages=find_packages(),
    install_requires=[
   	 'numpy',
   	 'pandas',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)

