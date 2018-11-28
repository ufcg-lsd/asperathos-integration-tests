from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='integration-tests',

    version='0.1.0',

    description='Integration tests for Asperathos framework',

    url='',

    author='Gabriel Silva Vinha',
    author_email='gabrielvinha@lsd.ufcg.edu.br',

    license='Apache 2.0',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: Apache 2.0',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',

    ],
    keywords='webservice application management asperathos integration tests',

    packages=find_packages(exclude=['contrib', 'docs', 'tmp']),

    install_requires=['requests']
)
