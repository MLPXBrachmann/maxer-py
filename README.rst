maxer
=====

*Maxer is a command line tool that enables easy batch image composition*

Getting started
---------------

First you need to install `libvips <https://jcupitt.github.io/libvips/install.html>`_.
Just follow their instructions and you'll be fine.

*Note:* Windows user have to set their PATH accordingly:

    $ setx path "%path%;C:\pathToVips\bin"

Then you can install Maxer using this command:

    $ pip install .

You can create a new Maxer project using

    $ maxer init <directory>

And build it using

    $ maxer

Help is available under

    $ maxer --help

Configuration
-------------

TODO

Notes
-----

- TODO: Check JSON before loading config
- TODO: Feature: Exists boolean operation
- TODO: If input string contains exactly one variable descriptor (and no additional characters): Resolve to variable value (do not stringify)
- TODO: Feature: More sophisticated output options (e.g. size, colorspace, etc.)
- TODO: Feature: Regex/split operation (extract part of other value)
- TODO: Feature: Read all files in folder
    - TODO: Feature: Load operation (read file list from folder)
    - TODO: Import field in config
- TODO: Feature: Map operation 
- TODO: Feature: Color manipulation operation
- TODO: Feature: Position/rotation/scale attributes on layer
- TODO: Feature: Blur attribute on layer
- TODO: Feature: Create solid layers by not providing 'file', but 'color' attribute
- TODO: Feature: Create shape layers by providing 'shape' attribute
- TODO: Preserve colorspace when recoloring/use 16bit color (+ premultiply?)
- TODO: Emit warning & continue if layer couldn't be loaded?
- TODO: Pre-resolve variables?
- TODO: Only use filename in output vs. identifyig path?
- TODO: Show file paths in output relative to main config file?

- Done: Resolve nested layer stacks

Development
-----------

If you've cloned this project, and want to install the library (*and all
development dependencies*), the command you'll want to run is::

    $ pip install -e .[test]

If you'd like to run all tests for this project (*assuming you've written
some*), you would run the following command::

    $ python setup.py test

This will trigger `pytest <http://pytest.org/latest/>`_, along with its popular
`coverage <https://pypi.python.org/pypi/pytest-cov>`_ plugin.

Lastly, if you'd like to cut a new release of this CLI tool, and publish it to
the Python Package Index (`PyPI <https://pypi.python.org/pypi>`_), you can do so
by running::

    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

This will build both a source tarball of your CLI tool, as well as a newer wheel
build (*and this will, by default, run on all platforms*).

The ``twine upload`` command (which requires you to install the `twine
<https://pypi.python.org/pypi/twine>`_ tool) will then securely upload your
new package to PyPI so everyone in the world can use it!
