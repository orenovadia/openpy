import io
from contextlib import contextmanager
from gzip import GzipFile
from urllib.parse import urlparse

from openpy.filesystem import FileSystem


@contextmanager
def _open_file(file_name):
    """
    open a local/s3 file whether uncompress if it is gzipped
    """
    parsed = urlparse(file_name)

    fs = FileSystem.get_filesystem(parsed.scheme)

    with fs.open(file_name) as f:
        if file_name.endswith('.gz') or file_name.endswith('.gzip'):
            f = GzipFile(fileobj=f)
        f = io.TextIOWrapper(f, encoding='utf-8')
        try:
            yield f
        finally:
            pass



open = _open_file
