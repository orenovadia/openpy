import io
from contextlib import contextmanager
from gzip import GzipFile


@contextmanager
def _open_file(file_name):
    """
    open a local/s3 file whether uncompress if it is gzipped
    """

    if file_name.startswith('s3://'):
        try:
            import s3fs
        except ImportError:
            raise ImportError("s3fs required for s3 files")
        handler = s3fs.S3FileSystem().open
    else:
        handler = io.open

    with handler(file_name, 'rb') as f:
        if file_name.endswith('.gz') or file_name.endswith('.gzip'):
            f = GzipFile(fileobj=f)
        f = io.TextIOWrapper(f, encoding='utf-8')
        try:
            yield f
        finally:
            pass


open = _open_file
