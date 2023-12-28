"""
@File       xcwarnings.py
@Brief      Module that detects new build warnings
@Author     rajaber
@Date       03-22-2021
@copyright  Microsoft Corporation. All rights reserved.
"""
import argparse
from collections import defaultdict
import json
import logging
import os
import re
import sys
from typing import ClassVar, Pattern


from xcwarnings.logger import create_logger
from xcwarnings.build_warning import BuildWarning, LocationalBuildWarning
from xcwarnings.build_warning_diff_report import BuildWarningDiffReport


class XcwarningsChecker:
    """A checker that detects new build warnings."""

    FILE_SCOPE_WARNING_PATTERN: ClassVar[Pattern] = re.compile(
        r"^(.*):(\d+):(\d+): warning: (.*)$"
    )
    TARGET_SCOPE_WARNING_PATTERN: ClassVar[Pattern] = re.compile(
        r"^warning: (.*) \(in target '(.*)' from project '(.*)'\)$"
    )
    TYPE_CHECK_PATTERN: ClassVar[Pattern] = re.compile(
        r".* '.*' took [0-9]+ms to type-check \(limit: [0-9]+ms\)"
    )

    xcodebuild_log_path: str
    defined_issues_file_path: str
    source_root: str
    skip_type_checks: bool
    log: logging.Logger

    def __init__(
        self,
        xcodebuild_log_path: str,
        defined_issues_file_path: str,
        source_root: str,
        skip_type_checks: str = False,
        log: logging.Logger | None = None,
    ):
        self.xcodebuild_log_path = xcodebuild_log_path
        self.defined_issues_file_path = defined_issues_file_path
        self.source_root = os.path.normpath(source_root)
        self.skip_type_checks = skip_type_checks

        if log:
            self.log = log.getChild(__name__)
        else:
            self.log = create_logger(__name__)

    def read_known_issues(self) -> dict[BuildWarning, int]:
        """Reads known build issues per optional configuration file.

        :returns: Dictionary of known build issues where the keys are the warnings of type BuildWarning,
        and the values are the counts of how many such warnings are expected in their respective files
        or project targets.
        Note: Those BuildWarning instances are not expected to contain line and column numbers because
        those tend to change as new content is added/removed.
        """

        return self.read_issues(self.defined_issues_file_path)

    def read_issues(self, issues_path: str) -> dict[BuildWarning, int]:
        """Reads build issues per the specified configuration file.

        :returns: Dictionary of build issues where the keys are the warnings of type BuildWarning,
        and the values are the counts of how many such warnings are expected in their respective files
        or project targets.
        Note: Those BuildWarning instances are not expected to contain line and column numbers because
        those tend to change as new content is added/removed.
        """

        with open(issues_path, encoding="utf-8") as file:
            data_file = file.read()

        issues_list = json.loads(data_file)

        return {
            LocationalBuildWarning.from_dict(issue): issue["count"]
            for issue in issues_list
        }

    def scan_line_for_warning(self, line: str) -> BuildWarning | None:
        """Scans given line from build output for a warning.

        :param line: Contents of a line of a build output file (as a string)

        :returns: BuildWarning instance or None if no warning is found in this line.
        """

        file_scope_warning_search = XcwarningsChecker.FILE_SCOPE_WARNING_PATTERN.search(
            line
        )

        if file_scope_warning_search:
            file_path = os.path.normpath(file_scope_warning_search.group(1))
            line_number = int(file_scope_warning_search.group(2))
            column = int(file_scope_warning_search.group(3))
            warning_statement = file_scope_warning_search.group(4)

            if not (file_path + os.sep).startswith(
                os.path.abspath(self.source_root) + os.sep
            ):
                # Exclude files not under source root
                return None

            relative_file_path = os.path.relpath(file_path, self.source_root)
            build_warning = LocationalBuildWarning.create_locational_file_warning(
                relative_file_path, line_number, column, warning_statement
            )
            return build_warning

        target_scope_warning_search = (
            XcwarningsChecker.TARGET_SCOPE_WARNING_PATTERN.search(line)
        )
        if target_scope_warning_search:
            warning_statement = target_scope_warning_search.group(1)
            target = target_scope_warning_search.group(2)
            project = target_scope_warning_search.group(3)
            build_warning = BuildWarning.create_target_warning(
                target, project, warning_statement
            )
            return build_warning

        return None

    def scan_for_warnings(self) -> [BuildWarning]:
        """Scans the given file for all build warnings

        :returns: An array of BuildWarning instances found. Empty array if none is found.
        Note: there may be duplicate build warnings if output file contains multiple lines refering to
        the same warning messages. They will show up as duplicate entries in the returned array.
        """
        with open(self.xcodebuild_log_path, encoding="utf-8") as file:
            data_file = file.readlines()

        warnings: [BuildWarning] = []

        for line in data_file:
            warning = self.scan_line_for_warning(line)
            if not warning:
                continue

            if self.skip_type_checks and XcwarningsChecker.TYPE_CHECK_PATTERN.match(
                warning.warning_statement
            ):
                continue

            warnings.append(warning)

        return warnings

    def get_warnings(self) -> set[BuildWarning]:
        """Gets all warnings found in given output file, deduped, and aggregated on the file level.

        :returns: An array of BuildWarning instances found. Empty array if none is found.
        Note: Duplicate build warnings in the output file with multiple lines refering to
        the same warning messages are deduped and will count as one error.
        """

        self.log.info(
            f"Extracting warnings from build output file: {self.xcodebuild_log_path}"
        )

        warnings = self.scan_for_warnings()
        warnings_deduped = set(warnings)
        self.log.info(
            f"Total number of warning instances found in build log file: {len(warnings_deduped)}."
        )

        return warnings_deduped

    @staticmethod
    def get_aggregated_warnings(
        warnings: set[LocationalBuildWarning | BuildWarning],
    ) -> dict[BuildWarning, int]:
        """Aggregates warnings so that all warnings in one file or target, have one entry in the output dictionary
        along with a count of how many times it occured

        :param warnings: Array of warnings found

        :returns: A dictionary of BuildWarning instances found. Each entry corresponds to one file or project/target.
        """

        warning_dict: dict[BuildWarning, int] = defaultdict(int)
        for warning in warnings:
            if isinstance(warning, LocationalBuildWarning):
                warning_dict[warning.locationless_copy()] += 1
            else:
                warning_dict[warning] += 1

        return warning_dict

    def generate_baseline(self) -> None:
        """Gets baseline for all known issues identified in the output file path, and writes them
        to a known issues file at the given path.

        This writes known issues in JSON format at output_known_issues_file.
        """

        self.log.info("Generating baseline 📈")
        warnings = self.get_warnings()
        warnings_with_count = XcwarningsChecker.get_aggregated_warnings(warnings)
        supressions = []

        for unique_warning, count in warnings_with_count.items():
            supression_entry = unique_warning.to_dict()
            supression_entry["count"] = count
            supressions.append(supression_entry)

        supressions.sort(
            key=lambda s: (
                s.get("project", ""),
                s.get("target", ""),
                s.get("file_path", ""),
                s.get("warning", ""),
            )
        )

        known_issues_json = json.dumps(supressions, indent=4)

        with open(self.defined_issues_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(known_issues_json)

        self.log.info(f"Baseline generated at file: {self.defined_issues_file_path}")

    def analyze(
        self,
    ) -> BuildWarningDiffReport:
        """Compares warnings present in the given output file with known warnings in
        defined_issues_file_path.

        :returns: An instance of BuildWarningDiffReport
        """
        known_issues = self.read_known_issues()
        current_warnings = self.get_warnings()
        aggregated_warnings = XcwarningsChecker.get_aggregated_warnings(
            current_warnings
        )
        return BuildWarningDiffReport.calculate_diff_report(
            known_issues, aggregated_warnings, current_warnings, self.log
        )


def handle_arguments() -> int:
    """Parses xcode build output file, and confirms there are no new warning errors.
    When --generate_baseline argument is passed, a baseline is generated with warnings found
    in given output log.

    :returns: An exit code signifying success or failure of the build warnings gate.
    """

    log = create_logger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--xcodebuild-log-path",
        dest="xcodebuild_log_path",
        help="Path to the xcodebuild output file",
        required=True,
    )
    parser.add_argument(
        "--defined-issues-file-path",
        dest="defined_issues_file_path",
        required=True,
        help="Full path to a JSON file with known build warnings",
    )
    parser.add_argument(
        "--source-root",
        dest="source_root",
        required=True,
        help="File path for the root of the source code",
    )
    parser.add_argument(
        "--generate-baseline",
        action="store_true",
        default=False,
        help="Whether a new baseline of known issues should be generated.",
    )

    args = parser.parse_args()

    log.info("Staring Build Warnings Detector ⚠️ ")

    checker = XcwarningsChecker(
        args.xcodebuild_log_path,
        args.defined_issues_file_path,
        args.source_root,
        log,
    )

    if args.generate_baseline:
        checker.generate_baseline()
        return 0

    log.info("Analyzing current warnings against known issues if any🔬.")
    diff_report = checker.analyze()
    log.info("Build Warnings Gate finished running. 🔥")
    return 0 if diff_report.success() else 1


if __name__ == "__main__":
    sys.exit(handle_arguments())
