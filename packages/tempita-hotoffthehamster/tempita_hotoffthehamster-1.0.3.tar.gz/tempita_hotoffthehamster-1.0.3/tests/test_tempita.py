import doctest
import unittest


class TestTempita(unittest.TestCase):
    def test_docs(self):
        doctest.testfile("../docs/index.rst")

    def test_readme(self):
        doctest.testfile("../README.rst")

    def test_templating(self):
        doctest.testfile("test_template.txt")
