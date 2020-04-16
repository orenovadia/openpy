import typing
from abc import ABC, abstractmethod
from typing import Type


class FileSystem(ABC):
    @classmethod
    def get_filesystem(cls, schema: str) -> 'FileSystem':
        for sub in FileSystem.__subclasses__():  # type: Type[FileSystem]
            if sub.services(schema):
                return sub()
        raise ValueError(f'No filesystem registered for "{schema}"')

    @classmethod
    @abstractmethod
    def services(cls, schema: str) -> bool:
        pass

    @abstractmethod
    def open(self, filename) -> typing.BinaryIO:
        pass


class LocalFileSystem(FileSystem):
    @classmethod
    def services(cls, schema: str) -> bool:
        return not schema

    def open(self, filename) -> typing.BinaryIO:
        return open(filename, 'rb')
