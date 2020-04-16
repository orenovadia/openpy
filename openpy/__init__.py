import binascii
import io
from contextlib import contextmanager
from gzip import GzipFile
from typing import BinaryIO
from urllib.parse import urlparse

from openpy.filesystem import FileSystem


@contextmanager
def _open_file(file_name):
    """
    open a local/s3 file whether uncompress if it is gzipped
    """
    parsed = urlparse(file_name)

    fs = FileSystem.get_filesystem(parsed.scheme)

    with fs.open(file_name) as binary_io:
        with _compression_wrapper(file_name, binary_io) as uncompressed:
            text = io.TextIOWrapper(uncompressed, encoding='utf-8')
            try:
                yield text
            finally:
                pass


def _compression_wrapper(file_name: str, f: BinaryIO):
    if file_name.endswith('.gz') or file_name.endswith('.gzip'):
        return GzipFile(fileobj=f)

    has_header = binascii.hexlify(f.read(2)) == b'1f8b'
    f.seek(0)
    if has_header:
        return GzipFile(fileobj=f)
    return f


open = _open_file
