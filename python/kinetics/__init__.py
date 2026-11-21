"""Compatibility namespace for the former kinetics package.

The maintained implementation now lives in :mod:`molecularis`. These aliases
preserve existing imports while callers migrate to the canonical package.
"""
import molecularis as _molecularis
from molecularis import *

__all__ = _molecularis.__all__
