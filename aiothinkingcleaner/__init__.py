"""Library to communicate with a Thinking Cleaner module asynchronously"""

import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata

from .thinkingcleaner import ThinkingCleaner


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()

__all__ = ["ThinkingCleaner"]
