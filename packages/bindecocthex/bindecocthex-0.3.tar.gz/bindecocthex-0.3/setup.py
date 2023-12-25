from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name='bindecocthex',
    version='0.3',
    description='A package for binary, decimal, octal, and hexadecimal conversions',
    author='Suriya Ravichandran, Karthikeyan Ramesh',
    author_email='rsuriya119@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://git.selfmade.ninja/rsuriya/bindecocthex',
    license='MIT',
    keywords=['python', 'binary', 'decimal', 'octal', 'hexadecimal', 'converter'],
)
