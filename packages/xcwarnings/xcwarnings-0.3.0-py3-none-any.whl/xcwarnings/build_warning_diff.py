"""
@File       build_warning_diff.py
@Brief      Build warning diff based on analyzing current warnings against known issues.
@Author     rajaber
@Date       03-22-2021
@copyright  Microsoft Corporation. All rights reserved.
"""
from xcwarnings.build_warning import BuildWarning


class BuildWarningDiff:
    """Holds counts for a given build warning: expected and actual counts"""

    def __init__(
        self, build_warning: BuildWarning, known_count: int, new_count: int
    ) -> None:
        self.build_warning = build_warning
        self.known_count = known_count
        self.new_count = new_count

    def __repr__(self) -> str:
        return f"({self.build_warning}, known count = {self.known_count}, new count = {self.new_count})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BuildWarningDiff):
            return False

        return (
            (self.build_warning == other.build_warning)
            and (self.known_count == other.known_count)
            and (self.new_count == other.new_count)
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.build_warning, self.known_count, self.new_count))
