"""The base command"""


class Base(object):
    """A base command"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Execute command"""
        raise NotImplementedError('This operation is not yet implemented.')
