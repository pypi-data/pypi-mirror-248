from setuptools import setup,find_packages
import os

requirements = os.popen('pipreqs bindecocthex --print').read().splitlines()

with open('README.md','r') as file:
    long_description = file.read()
    
setup(
    name='bindecocthex',
    version='0.2',
    description='A package for binary, decimal, octal, and hexadecimal conversions',
    author='Suriya Ravichandran,Karthikeyan Ramesh',
    author_email='rsuriya119@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.selfmade.ninja/rsuriya/bindecocthex',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'bindecocthex=bindecocthex:main',
        ],
    },
)
