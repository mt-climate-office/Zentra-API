from ..api import Extension
from ..api import helpers

MY_AWESOME_FILE = """\
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "{author}"
__copyright__ = "{author}"
__license__ = "${license}"

def awesome():
    return "Awesome!"
"""

MY_AWESOME_TEST = """\
import pytest
from {qual_pkg}.awesome import awesome

def test_awesome():
    assert awesome() == "Awesome!"
"""


class AwesomeFiles(Extension):
    """Adding some additional awesome files"""

    def activate(self, actions):
        return helpers.register(actions, self.define_awesome_files)

    def define_awesome_files(self, struct, opts):
        struct = helpers.merge(struct, {
            opts['project']: {
                opts['package']: {
                    'awesome.py': MY_AWESOME_FILE.format(**opts)
                },
                'tests': {
                    'awesome_test.py': (
                        MY_AWESOME_TEST.format(**opts),
                        helpers.NO_OVERWRITE
                    )
                }
            }
        })

        struct['.python-version'] = ('3.6.1', helpers.NO_OVERWRITE)

        for filename in ['awesome_file1', 'awesome_file2']:
            struct = helpers.ensure(
                struct, [opts['project'], 'awesome', filename],
                content='AWESOME!', update_rule=helpers.NO_CREATE)
            # The second argument is the file path, represented by a
            # list of file parts or a string.
            # Alternatively in this example:
            # path = '{project}/awesome/{filename}'.format(
            #           filename=filename, **opts)

        # The `reject` can be used to avoid default files being generated.
        struct = helpers.reject(
            struct, '{project}/{package}/skeleton.py'.format(**opts))
        # Alternatively in this example:
        # path = [opts['project'], opts['package'], 'skeleton.py'])

        # It is import to remember the return values
        return struct, opts
