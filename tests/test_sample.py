from unittest import TestCase
import openpy


class OpenTests(TestCase):
    def test_local_file(self):
        with openpy.open(__file__) as f:
            contents = f.read()
        self.assertTrue('this particular string' in contents)

    def test_utf8_file(self):
        with openpy.open('utf8.txt') as f:
            contents = f.read()
        self.assertTrue('hi 😀' in contents)

    def test_local_gzipped_file(self):
        with openpy.open('gzipped.gz') as f:
            contents = f.read()
        self.assertTrue('this string' in contents)
