"""The init command"""


import json
import os

from ..lib import ensure_dir, print_done, print_error, print_info

from .base import Base

BASE_CONFIG = {
    'output': {
        'baseDir': 'output',
        'file': 'result.png',
    },
    'input': {
        'baseDir': 'input',
        'layers': [
            {
                'file': 'input.png',
                'color': 'retain',
                'blendMode': 'over',
            },
            'background.png',
        ],
    },
    'palette': {},
    'combinations': [{}],
}

class Init(Base):
    """Initialize new maxer project"""

    def run(self):
        directory = os.path.join(os.getcwd(), self.options['<directory>'] or '')
        config_file = os.path.join(directory, 'maxer.json')

        if os.path.exists(config_file):
            print_error('\'maxer.json\' already exists')
            raise SystemExit(1)

        # Create directories
        ensure_dir(os.path.join(directory, 'input'))
        ensure_dir(os.path.join(directory, 'output'))

        # Create config
        with open(config_file, 'w') as json_data:
            json.dump(BASE_CONFIG, json_data, indent=2)

        print_info('Created config: \'{}\''.format(config_file))
        print_done('Done.')
