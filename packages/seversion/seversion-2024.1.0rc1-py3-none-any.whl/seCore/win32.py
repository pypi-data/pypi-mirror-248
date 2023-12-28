"""
Win32 utilities.

@var O_BINARY: the 'binary' mode flag on Windows, or 0 on other platforms, so it
    may safely be OR'ed into a mask for os.open.
"""

import os

# https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes
ERROR_FILE_NOT_FOUND = 2
ERROR_PATH_NOT_FOUND = 3
ERROR_INVALID_NAME = 123
ERROR_DIRECTORY = 267

O_BINARY = getattr(os, "O_BINARY", 0)
