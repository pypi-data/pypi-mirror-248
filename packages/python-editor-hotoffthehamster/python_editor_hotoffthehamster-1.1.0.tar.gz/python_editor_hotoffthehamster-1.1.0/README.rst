@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
python-editor-hotoffthehamster
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. CXREF:
   https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge

.. image:: https://github.com/doblabs/python-editor-hotoffthehamster/actions/workflows/checks-unspecial.yml/badge.svg?branch=release
  :target: https://github.com/doblabs/python-editor-hotoffthehamster/actions/workflows/checks-unspecial.yml/badge.svg?branch=release
  :alt: Build Status

.. CXREF: https://app.codecov.io/github.com/doblabs/python-editor-hotoffthehamster/settings/badge

.. image:: https://codecov.io/gh/doblabs/python-editor-hotoffthehamster/branch/release/graph/badge.svg?token=XXX
  :target: https://app.codecov.io/gh/doblabs/python-editor-hotoffthehamster
  :alt: Coverage Status

.. image:: https://readthedocs.org/projects/python-editor-hotoffthehamster/badge/?version=latest
  :target: https://python-editor-hotoffthehamster.readthedocs.io/en/latest/
  :alt: Documentation Status

.. image:: https://img.shields.io/github/v/release/doblabs/python-editor-hotoffthehamster.svg?style=flat
  :target: https://github.com/doblabs/python-editor-hotoffthehamster/releases
  :alt: GitHub Release Status

.. image:: https://img.shields.io/pypi/v/python-editor-hotoffthehamster.svg
  :target: https://pypi.org/project/python-editor-hotoffthehamster/
  :alt: PyPI Release Status

.. image:: https://img.shields.io/pypi/pyversions/python-editor-hotoffthehamster.svg
  :target: https://pypi.org/project/python-editor-hotoffthehamster/
  :alt: PyPI Supported Python Versions

.. image:: https://img.shields.io/github/license/doblabs/python-editor-hotoffthehamster.svg?style=flat
  :target: https://github.com/doblabs/python-editor-hotoffthehamster/blob/release/LICENSE
  :alt: License Status

.. |dob| replace:: ``dob``
.. _dob: https://github.com/doblabs/dob

.. |python-editor| replace:: ``python-editor``
.. _python-editor: https://github.com/fmoo/python-editor

|

|python-editor|_ revival fork for |dob|_ (because ``python-editor`` has not
been released `in many years <https://pypi.org/project/python-editor/>`__.

###############
Original README
###############

``python-editor`` is a library that provides the ``editor`` module for
programmatically interfacing with your system's $EDITOR.

Examples
========

.. code-block::  python

  import editor
  commit_msg = editor.edit(contents=b"# Enter commit message here")

Opens an editor, prefilled with the contents, ``# Enter commit message here``.
When the editor is closed, returns the contents (bytes) in variable ``commit_msg``.
Note that the argument to ``contents`` needs to be a bytes object on Python 3.

.. code-block::  python

  editor.edit(file="README.txt")

Opens ``README.txt`` in an editor.  Changes are saved in place.  If there is
a ``contents`` argument then the file contents will be overwritten.

.. code-block::  python

  editor.edit(..., use_tty=True)

Opens the editor in a TTY.  This is usually done in programs which output is
piped to other programs.  In this case the TTY is used as the editor's stdout,
allowing interactive usage.

How it Works
============

``editor`` first looks for the ``${EDITOR}`` environment variable.  If set, it uses
the value as-is, without fallbacks.

If no $EDITOR is set, editor will search through a list of known editors, and
use the first one that exists on the system.

For example, on Linux, ``editor`` will look for the following editors in order:

* ``vim``
* ``emacs``
* ``nano``

When calling ``editor.edit``, an editor will be opened in a subprocess, inheriting
the parent process's stdin, stdout.
