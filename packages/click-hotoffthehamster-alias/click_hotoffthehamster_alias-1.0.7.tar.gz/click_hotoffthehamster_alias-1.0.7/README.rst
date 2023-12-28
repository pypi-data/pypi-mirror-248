@@@@@@@@@@@@@@@@@@@@@@@@@@@@
click-hotoffthehamster-alias
@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. CXREF:
   https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge

.. image:: https://github.com/doblabs/easy-as-pypi/actions/workflows/checks-unspecial.yml/badge.svg?branch=release
  :target: https://github.com/doblabs/easy-as-pypi/actions/workflows/checks-unspecial.yml/badge.svg?branch=release
  :alt: Build Status

.. CXREF: https://app.codecov.io/github.com/doblabs/easy-as-pypi/settings/badge

.. image:: https://codecov.io/gh/doblabs/easy-as-pypi/branch/release/graph/badge.svg?token=AlKUyOgTGY
  :target: https://app.codecov.io/gh/doblabs/easy-as-pypi
  :alt: Coverage Status

.. image:: https://readthedocs.org/projects/easy-as-pypi/badge/?version=latest
  :target: https://easy-as-pypi.readthedocs.io/en/latest/
  :alt: Documentation Status

.. image:: https://img.shields.io/github/v/release/doblabs/easy-as-pypi.svg?style=flat
  :target: https://github.com/doblabs/easy-as-pypi/releases
  :alt: GitHub Release Status

.. image:: https://img.shields.io/pypi/v/easy-as-pypi.svg
  :target: https://pypi.org/project/easy-as-pypi/
  :alt: PyPI Release Status

.. image:: https://img.shields.io/pypi/pyversions/easy-as-pypi.svg
  :target: https://pypi.org/project/easy-as-pypi/
  :alt: PyPI Supported Python Versions

.. image:: https://img.shields.io/github/license/doblabs/easy-as-pypi.svg?style=flat
  :target: https://github.com/doblabs/easy-as-pypi/blob/release/LICENSE
  :alt: License Status

|

Add (multiple) aliases to a ``click`` group or command.

In your `click <http://click.pocoo.org/>`__ app:

.. code-block:: python

  import click_hotoffthehamster as click
  from click_hotoffthehamster import ClickAliasedGroup

   @click.group(cls=ClickAliasedGroup)
   def cli():
       pass

   @cli.command(aliases=['bar', 'baz', 'qux'])
   def foo():
       """Run a command."""
       click.echo('foo')

Will result in::

   Usage: cli [OPTIONS] COMMAND [ARGS]...

   Options:
     --help  Show this message and exit.

   Commands:
     foo (bar,baz,qux)  Run a command.

