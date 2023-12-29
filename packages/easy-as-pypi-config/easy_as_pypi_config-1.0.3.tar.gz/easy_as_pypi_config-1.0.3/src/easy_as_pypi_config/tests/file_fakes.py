# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Useful generic file fixtures."""

import os
import sys
import tempfile

import fauxfactory
import py
import pytest

# 2023-11-13: GHA macOS py3.12 will sometimes die on gen_utf8 filenames,
# e.g.,
#   tests/test_fileboss.py:227: in simple_config_obj
#     with open(filepath, "w") as conf_file:
# Or, e.g.,
#   tests/test_urable.py:233: in test_write_config
#     configurable.write_config()
# In either case raising, e.g.,
#   OSError: [Errno 92] Illegal byte sequence: '.../拴蛡リ덐𑤯ᑲꜙⳁ𞁅劂'
# One work-around I tried was hoping to normalize the filename for macOS:
#   unicodedata.normalize("NFC", filename)
# But that didn't work.
#
# Given that this is the only OS with this issue, and it's intermittently
# failing CI checks, we'll just not use UTF8 filenames on macOS.


@pytest.fixture
def filename():
    """Provide a filename string."""
    if sys.platform.startswith("darwin"):
        # TRACK/2023-12-22: If gen_latin1 also fails on macOS CI,
        # then consider another generator:
        #   gen_cjk, gen_cyrillic, gen_alphanumeric
        return fauxfactory.gen_latin1()
    else:
        return fauxfactory.gen_utf8()

    return filename


@pytest.fixture
def filepath(tmpdir, filename):
    """Provide a fully qualified pathame within our tmp-dir."""
    return os.path.join(tmpdir.strpath, filename)


@pytest.fixture(scope="session")
def tmpdir_ro(request):
    # https://stackoverflow.com/questions/25525202/py-test-temporary-folder-for-the-session-scope
    # Make a temporary directory, and wrap the path string in a Path object,
    # so that `.remove` works, and so test fixtures can treat it same as a
    # `tmpdir` builtin pytest fixture.
    _tmpdir = py.path.local(tempfile.mkdtemp())
    request.addfinalizer(lambda: _tmpdir.remove(rec=1))
    return _tmpdir
