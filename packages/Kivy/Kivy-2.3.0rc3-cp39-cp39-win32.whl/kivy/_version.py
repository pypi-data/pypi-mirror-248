# This file is imported from __init__.py and exec'd from setup.py

MAJOR = 2
MINOR = 3
MICRO = 0
RELEASE = False

__version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

if not RELEASE:
    # if it's a rcx release, it's not proceeded by a period. If it is a
    # devx release, it must start with a period
    __version__ += 'rc3'


_kivy_git_hash = 'c1d89471bb60a3b19fa017e2df9fe64ad0bd67a0'
_kivy_build_date = '20240101'

