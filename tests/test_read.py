from pathlib import Path
from unittest import TestCase, skip

import openpy


class OpenTests(TestCase):
    def test_local_file(self):
        contents = self._read_local(__file__)
        self.assertTrue('this particular string' in contents)

    def test_utf8_file(self):
        contents = self._read_local('utf8.txt')
        self.assertTrue('hi 😀' in contents)

    def test_local_gzipped_file(self):
        contents = self._read_local('gzipped.gz')
        self.assertTrue('this string' in contents)

    def test_local_gzipped_file_without_extension(self):
        contents = self._read_local('gzipped_file_without_extention')
        self.assertTrue('this string' in contents)

    def test_http_plain(self):
        contents = self._read('http://raw.githubusercontent.com/orenovadia/openpy/master/README.md')
        self.assertTrue('openpy' in contents)

        contents = self._read('https://raw.githubusercontent.com/orenovadia/openpy/master/README.md')
        self.assertTrue('openpy' in contents)

    def test_http_zipped(self):
        contents = self._read('https://github.com/orenovadia/openpy/raw/master/tests/gzipped.gz')
        self.assertTrue('this string' in contents)

    @skip('slow')
    def test_s3_plain(self):
        path_to_public_data_in_s3 = 's3://gdc-target-phs000218-2-open/2134dc56-81e2' \
                                    '-4a77-bfa6-24d6fb764599/5e5edf30-89da-457a-b227-87052b1c8a5d_analysis.xml'
        with openpy.read(path_to_public_data_in_s3) as f:
            self.assertTrue('analysis_xml' in next(f))

    def _read_local(self, path):
        full_path = Path(__file__).cwd() / path
        return self._read(str(full_path))

    def _read(self, path):
        with openpy.read(path) as f:
            return f.read()
