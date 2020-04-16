import binascii
import io
from contextlib import contextmanager
from gzip import GzipFile
from typing import BinaryIO
from urllib.parse import urlparse

from openpy.filesystem import FileSystem


def compression_wrapper(file_name: str, f: BinaryIO):
    needs_gzip = False
    if file_name.endswith('.gz') or file_name.endswith('.gzip'):
        return GzipFile(fileobj=f)

    has_header = binascii.hexlify(f.read(2)) == b'1f8b'
    f.seek(0)
    if has_header:
        return GzipFile(fileobj=f)
    return f


@contextmanager
def _open_file(file_name):
    """
    open a local/s3 file whether uncompress if it is gzipped
    """
    parsed = urlparse(file_name)

    fs = FileSystem.get_filesystem(parsed.scheme)

    with fs.open(file_name) as f:
        with compression_wrapper(file_name, f) as f:
            f = io.TextIOWrapper(f, encoding='utf-8')
            try:
                yield f
            finally:
                pass


open = _open_file
