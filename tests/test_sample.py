from unittest import TestCase

import openpy


class OpenTests(TestCase):
    def test_local_file(self):
        contents = self._read(__file__)
        self.assertTrue('this particular string' in contents)

    def test_utf8_file(self):
        contents = self._read('utf8.txt')
        self.assertTrue('hi 😀' in contents)

    def test_local_gzipped_file(self):
        contents = self._read('gzipped.gz')
        self.assertTrue('this string' in contents)

    def test_s3_plain(self):
        path_to_public_data_in_s3 = 's3://gdc-target-phs000218-2-open/2134dc56-81e2' \
                                    '-4a77-bfa6-24d6fb764599/5e5edf30-89da-457a-b227-87052b1c8a5d_analysis.xml'
        with openpy.open(path_to_public_data_in_s3) as f:
            self.assertTrue('analysis_xml' in next(f))

    def _read(self, path):
        with openpy.open(path) as f:
            return f.read()
