"""
maxer

Usage:
  maxer init [<directory>]
  maxer check [<config>]
  maxer [build] [<config>]
  maxer -h | --help
  maxer --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  maxer init
  maxer
"""

import colorama
from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint"""

    from maxer import commands
    options = docopt(__doc__, version=VERSION)

    colorama.init()

    command = commands.Init if options['init'] else (
        commands.Check if options['check'] else commands.Build
    )
    # TODO: Only use run method/static run method
    command = command(options)
    command.run()
