"""Unit test for pykabutan.__version__."""

import re

import pykabutan as pk


def test_version_looks_like_a_version_string():
    assert isinstance(pk.__version__, str)
    assert pk.__version__
    assert re.match(r"\d+\.\d+", pk.__version__)
