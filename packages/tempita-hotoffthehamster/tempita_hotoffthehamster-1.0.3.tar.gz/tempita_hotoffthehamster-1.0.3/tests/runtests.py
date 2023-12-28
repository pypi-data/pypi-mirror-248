#!/usr/bin/env python3

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import doctest  # noqa: E402

if __name__ == "__main__":
    doctest.testfile("test_template.txt")
    doctest.testfile("../docs/index.txt")
