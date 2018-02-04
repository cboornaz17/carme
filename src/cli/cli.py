"""
carme

Usage:
  carme -h | --help
  carme -v | --version
  carme hello
  carme new <project>

Options:
  -h --help                         Show this screen.
  -v --version                      Show version.
  -f --force                        Force.
  --jupyter                         Set config to include jupyter.
  --echo                            Only print the comand, don't execute.

Examples:
  carme cluster new

Help:
  For help using this tool, please see the Github repository:
  https://github.com/carme/carme
"""
#TODO Update the helptext above. Preferably move it to somewhere better.

from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION
from os.path import abspath, dirname, join, isfile
import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase

def run(command):
    print(command)
    input=command.split()
    if input[0]!="kubel":
        input.insert(0,"kubel")
    return popen(input, stdout=PIPE).communicate()[0]

def main():
    """Main CLI entrypoint."""
    #print(__doc__)
    options = docopt(__doc__, version=VERSION)
    cli(options)

def cli(options):
    import src.cli.commands as kc
    """Main CLI entrypoint."""
    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
          if hasattr(kc, k) and v:
            module = getattr(kc, k)
            kc = getmembers(module, isclass)
            print("kc",kc)
            command = [command[1] for command in kc if command[0] != 'Base'][0]
            command = command(options)
            command.run()

if __name__ == "__main__":
    main() # Don't forget to actually run main!