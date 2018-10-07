"""Packaging settings"""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from maxer import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

class RunTests(Command):
    """Run all tests"""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run tests"""
        errno = call(['pytest', '--cov=maxer', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name='maxer',
    version=__version__,
    description='A tool for layer-based batch image processing.',
    long_description=long_description,
    # url='',
    author='Paul Brachmann',
    author_email='paul@malpaux.com',
    license='UNLICENSED',
    classifiers=[
        'Intended Audience :: Designers & Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['colorama', 'colour', 'docopt', 'pyvips'],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'maxer=maxer.cli:main',
        ],
    },
    cmdclass={'test': RunTests},
)
