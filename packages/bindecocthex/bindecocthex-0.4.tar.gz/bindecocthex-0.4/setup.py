from setuptools import setup, find_packages

setup(
    name='bindecocthex',
    version='0.4',
    packages=['bindecocthex'],
    package_data={
        '': ['README.md'],
    },
    entry_points={
        'console_scripts': [
            'bindecocthex = bindecocthex.conversion:main'
        ]
    },
    install_requires=[
        # List your dependencies here
    ],
    python_requires='>=3.6',
    author='Suriya Ravichandran',
    author_email='rsuriya119@gmail.com',
    description='A library for binary, decimal, octal, and hexadecimal conversions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://git.selfmade.ninja/rsuriya/bindecocthex',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    data_files=[('', ['LICENSE'])],
)
