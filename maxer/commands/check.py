"""The check command"""


import os

from ..lib import check_config, load_config, print_done, print_error

from .base import Base

class Check(Base):
    """Check a maxer config"""

    # TODO: Soundness check (multiple level can be set, up to checking if files exist/running without writing)
    def run(self):
        config_file = os.path.join(os.getcwd(), self.options['<config>'] or 'maxer.json')
        try:
            config = load_config(config_file)
            if check_config(config):
                print_done('Check successfully completed.')
            else:
                print_error('Invalid config')
                raise SystemExit(1)
        except IOError:
            print_error('Unable to read config \'{}\''.format(os.path.basename(config_file)))
            raise SystemExit(1)
