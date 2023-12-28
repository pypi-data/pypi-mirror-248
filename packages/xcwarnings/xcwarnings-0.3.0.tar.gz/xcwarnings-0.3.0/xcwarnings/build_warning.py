"""
@File       build_warning.py
@Brief      An Xcode build warning
@Author     rajaber
@Date       03-22-2021
@copyright  Microsoft Corporation. All rights reserved.
"""

from typing import Union

from xcwarnings.build_warning_scope import BuildWarningScope


class BuildWarning:
    # pylint: disable = too-many-arguments
    """BuildWarning contains metadata about a warning in an xcode build output file"""

    def __init__(
        self,
        file_path: str | None,
        target: str | None,
        project: str | None,
        warning_statement: str,
    ) -> None:
        self.file_path = file_path
        self.target = target
        self.project = project
        self.warning_statement = warning_statement
        if self.file_path is not None:
            self.scope = BuildWarningScope.FILE
        else:
            self.scope = BuildWarningScope.TARGET

    # pylint: enable = too-many-arguments

    def __repr__(self) -> str:
        if self.scope == BuildWarningScope.FILE:
            return (
                f"BuildWarning(Warning in file: {self.file_path}. "
                + f"Warning: {self.warning_statement})"
            )

        if self.scope == BuildWarningScope.TARGET:
            return (
                f"BuildWarning(Warning in target: {self.target}. "
                + f"Project: {self.project}. Warning: {self.warning_statement})"
            )

        raise ValueError(f"Unexpected scope: {self.scope}")

    def __eq__(self, other: object):
        """Checks if currrent instance is eual to the other instance

        :param other: object to compare to current instance for equality

        :returns: True if objects are equal; otherwise, false.
        """
        if not isinstance(other, BuildWarning):
            return False

        return (
            (self.file_path == other.file_path)
            and (self.warning_statement == other.warning_statement)
            and (self.project == other.project)
            and (self.target == other.target)
        )

    def __ne__(self, other: object) -> bool:
        """Checks if currrent instance is not equal to the other instance

        :param other: object to compare to current instance for equality

        :returns: True if objects are not equal; otherwise, true.
        """
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns hash of current instance

        :returns: Hash of BuildWarning instance
        """
        return hash(self.__repr__())

    def to_dict(self) -> dict[str, object]:
        """Serializes BuildWarning instance into a dictionary."""
        warning_dict: dict[str, object] = {}
        warning_dict["warning"] = self.warning_statement
        if self.scope == BuildWarningScope.FILE:
            warning_dict["file_path"] = self.file_path
        elif self.scope == BuildWarningScope.TARGET:
            warning_dict["target"] = self.target
            warning_dict["project"] = self.project
        else:
            raise ValueError(f"Unexpected scope: {self.scope}")
        return warning_dict

    @staticmethod
    def create_file_warning(
        file_path: str,
        warning_statement: str,
    ) -> "BuildWarning":
        """Creates a file level warning

        :param file_path: Path to the file where the warning occurs, relative to the repo root.
        :param warning_statement: Warning statement

        :returns: A file level warning
        """
        return BuildWarning(file_path, None, None, warning_statement)

    @staticmethod
    def create_target_warning(
        target: str, project: str, warning_statement: str
    ) -> "BuildWarning":
        """Creates a target level warning

        :param target: Target where the warning occurs
        :param project: Project where the warning occurs
        :param warning_statement: Warning statement

        :returns: A target level warning
        """
        return BuildWarning(None, target, project, warning_statement)

    @staticmethod
    def from_dict(input_dict: dict[str, object]) -> "BuildWarning":
        """Creates an instance of BuildWarning from given dictinoary.

        :param input_dict: dictionary serialization of BuildWarning

        :returns: An instance of build warning
        """
        return BuildWarning(
            input_dict.get("file_path"),
            input_dict.get("target"),
            input_dict.get("project"),
            input_dict["warning"],
        )


class LocationalBuildWarning(BuildWarning):
    # pylint: disable = too-many-arguments
    """BuildWarning contains metadata about a warning in an xcode build output file"""

    def __init__(
        self,
        file_path: str | None,
        line_number: str,
        column: str,
        project: str | None,
        warning_statement: str,
    ) -> None:
        super().__init__(file_path, None, project, warning_statement)
        assert line_number is not None
        assert column is not None
        self.line_number = line_number
        self.column = column

    def locationless_copy(self) -> BuildWarning:
        """Return a version of self without the location information set."""
        return BuildWarning.from_dict(self.to_dict())

    # pylint: enable = too-many-arguments

    def __repr__(self) -> str:
        if self.scope == BuildWarningScope.FILE:
            return (
                f"LocationalBuildWarning(Warning in file: {self.file_path}:{self.line_number}:{self.column}. "
                + f"Warning: {self.warning_statement})"
            )

        if self.scope == BuildWarningScope.TARGET:
            return (
                f"LocationalBuildWarning(Warning in target: {self.target}. "
                + f"Project: {self.project}. Warning: {self.warning_statement})"
            )

        raise ValueError(f"Unexpected scope: {self.scope}")

    def __eq__(self, other: object):
        """Checks if currrent instance is eual to the other instance

        :param other: object to compare to current instance for equality

        :returns: True if objects are equal; otherwise, false.
        """
        if not isinstance(other, LocationalBuildWarning):
            return False

        if not super().__eq__(other):
            return False

        return (self.line_number == other.line_number) and (self.column == other.column)

    def __ne__(self, other: object) -> bool:
        """Checks if currrent instance is not equal to the other instance

        :param other: object to compare to current instance for equality

        :returns: True if objects are not equal; otherwise, true.
        """
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns hash of current instance

        :returns: Hash of BuildWarning instance
        """
        return hash(self.__repr__())

    def to_dict(self) -> dict[str, object]:
        """Serializes BuildWarning instance into a dictionary."""
        warning_dict = super().to_dict()
        if self.scope == BuildWarningScope.FILE:
            warning_dict["line_number"] = self.line_number
            warning_dict["column"] = self.column
        return warning_dict

    @staticmethod
    def create_locational_file_warning(
        file_path: str,
        line_number: int | None,
        column: int | None,
        warning_statement: str,
    ) -> "LocationalBuildWarning":
        """Creates a file level warning

        :param file_path: Path to the file where the warning occurs, relative to the repo root.
        :param line_number: Line number where the warning occurs
        :param column: Column within the line where the warning occurs
        :param warning_statement: Warning statement

        :returns: A file level warning
        """
        return LocationalBuildWarning(
            file_path, line_number, column, None, warning_statement
        )

    @staticmethod
    def from_dict(
        input_dict: dict[str, object]
    ) -> Union["LocationalBuildWarning", BuildWarning]:
        """Creates an instance of BuildWarning from given dictinoary.

        :param input_dict: dictionary serialization of BuildWarning

        :returns: An instance of build warning
        """

        if "line_number" in input_dict and "column" in input_dict:
            return LocationalBuildWarning(
                input_dict.get("file_path"),
                input_dict.get("line_number"),
                input_dict.get("column"),
                input_dict.get("project"),
                input_dict["warning"],
            )

        return BuildWarning.from_dict(input_dict)
