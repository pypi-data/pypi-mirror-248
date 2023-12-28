"""
@File       build_warning_scope.py
@Brief      Scope of a build warning
@Author     rajaber
@Date       03-22-2021
@copyright  Microsoft Corporation. All rights reserved.
"""
from enum import Enum

class BuildWarningScope(Enum):
    """Scope of a build warning"""
    FILE = 1
    TARGET = 2
