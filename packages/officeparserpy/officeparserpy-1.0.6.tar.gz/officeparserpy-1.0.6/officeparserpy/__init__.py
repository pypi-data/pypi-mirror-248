# __init__.py

from .officeparserpy import (
    parse_office,
    ExtensionUnsupported,
    FileCorrupted,
    FileDoesNotExist,
    ImproperBuffers,
    ImproperArguments,
    LocationNotFound
)

__all__ = [
    'parse_office',
    'ExtensionUnsupported',
    'FileCorrupted',
    'FileDoesNotExist',
    'ImproperBuffers',
    'ImproperArguments',
    'LocationNotFound'
]
