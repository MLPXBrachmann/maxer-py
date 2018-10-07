"""The build command."""


from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time

from ..lib import (
    check_config,
    composite_image,
    flatten,
    generate_combinations,
    invert_layer_order,
    load_config,
    MaxerResolveError,
    print_done,
    print_error,
    print_failed,
    print_start,
)

from .base import Base

class Build(Base):
    """Build a maxer project"""

    def run(self):
        pool = ThreadPoolExecutor()
        futures = []

        config_file = os.path.join(os.getcwd(), self.options['<config>'] or 'maxer.json')
        try:
            config = load_config(config_file)
        except IOError:
            print_error('Unable to read config \'{}\''.format(os.path.basename(config_file)))
            raise SystemExit(1)

        if not check_config(config):
            print_error('Invalid config')
            raise SystemExit(1)

        invert_layer_order(config)
        flatten(config['input']['layers'])

        start_time = time.perf_counter()

        combinations = generate_combinations(config)
        print_start('Building {} sets...'.format(str(len(combinations))))

        for combination in combinations:
            futures.append(
                pool.submit(composite_image, config, os.path.dirname(config_file), combination)
            )

        for future in as_completed(futures):
            try:
                future.result()
            except MaxerResolveError as err:
                print_error(str(err))
                print_failed('Failed')

        print_done('Done in {:.4f}s.'.format(time.perf_counter() - start_time))
