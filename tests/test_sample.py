from unittest import TestCase
import openpy


class OpenTests(TestCase):
    def test_local_file(self):
        with openpy.open(__file__) as f:
            contents = f.read()
        self.assertTrue('this particular string' in contents)
