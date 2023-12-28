# xcwarnings

**xcwarnings** is a tool that helps Xcode developers set up a quality gate to catch new build warnings introduced to their codebase. This gate is meant to run on Pull Requests or Continuous Integration pipelines.

[ [Features](#features) | [Requirements](#requirements) | [Installation](#installation) | [Usage](#usage) | [Running Tests](#running-tests) | [Contributing](#contributing) | [Trademarks](#trademarks) ]

## Features

- Checks for build warnings in your Xcode build output log, and fails if unexpected warnings are encountered.

- Can excludes a certain list of warnings, provided in an optional known warnings configuration file, from triggering a failure. The configuraiton file is easy to read and in JSON format.

- Generates a baseline known warnings file for current Xcode build output log. This is useful when onboarding to the tool, or when you're upgrading major Xcode version.

Note: If your project is already at zero warnings, you can turn all warnings into errors using the `Treat Warnings as Errors` build setting, and rely on the build failing.

## Requirements

- Python 3.6 or above
- Tested with logs from Xcode 12.4.

## Installation

```
$ pip install xcwarnings
```

Note: it is recommended to run the above commands in the context of a python 3 virtual environment. For more about setting one up, see [Getting Started with Python](docs/GetStartedWithPython.md).

## Usage

```
usage: xcwarnings.py [-h]
                 [--known_build_warnings_file_path KNOWN_BUILD_WARNINGS_FILE_PATH]
                 --source_root SOURCE_ROOT [--generate_baseline]
                 xcode_build_output_file_path

positional arguments:
  xcode_build_output_file_path
                        Path to the xcode output file

optional arguments:
  -h, --help            show this help message and exit
  --known_build_warnings_file_path KNOWN_BUILD_WARNINGS_FILE_PATH
                        Full path to a file with known build warnings
  --source_root SOURCE_ROOT
                        File path for the root of the source code
  --generate_baseline   Whether a new baseline of known issues should be
                        generated.
```

### Examples

#### Generating baseline configuration files

To generate a baseline configuration on the desktop, for the sample xcode log file at `./tests/xcwarnings_tests/test_output_file_warnings.txt`, you can run the command:

```
$ python3 -m xcwarnings.xcwarnings ./tests/xcwarnings_tests/test_output_file_warnings.txt \
          --known_build_warnings_file_path ~/Desktop/generated_known_issues.json \
          --source_root ~/Documents/XCWarningsDemo \
          --generate_baseline
```

To get a baseline for your project, you first compile your project, storing the output in a log file:

```
$ xcodebuild build -project [PATH_TO_YOUR_PROJ.xcodeproj] >~/Desktop/log_output.log
```

Followed by:

```
$ python3 -m xcwarnings.xcwarnings ~/Desktop/log_output.log \
          --known_build_warnings_file_path ~/Desktop/generated_known_issues.json \
          --source_root ~/Documents/XCWarningsDemo \
          --generate_baseline
```

#### Checking for regressions

To check whether xcode build log contains new warnings not referenced in a given configuration file:

```
$ python3 -m xcwarnings.xcwarnings ./tests/xcwarnings_tests/test_output_file_warnings.txt \
          --known_build_warnings_file_path ~/Desktop/generated_known_issues.json \
          --source_root ~/Documents/XCWarningsDemo
```

Note: it is recommended to run the above commands in the context of a python 3 virtual environment. For more about setting one up, see [Getting Started With Python](docs/GetStartedWithPython.md).

#### An Example Configuration File

Configuration file is expected to be in JSON format. It is an array of expected warning. Each warning should include the warning statement and the number of times it's expected. If the warning is at the file level, then file_path should be provided. file_path should be relative to SOURCE_ROOT. If the warning is at the target level, then target and project should be provided. See the example below.

```
[
    {
        "warning": "'statusBarOrientation' was deprecated in iOS 13.0: Use the interfaceOrientation property of the window scene instead.",
        "file_path": "XCWarningsDemo/ContentView.swift",
        "count": 2
    },
    {
        "warning": "'deprecatedApi()' is deprecated",
        "file_path": "XCWarningsDemo/ContentView.swift",
        "count": 1
    },
    {
        "warning": "AddressBookUI is deprecated. Consider migrating to ContactsUI instead.",
        "target": "XCWarningsDemoTarget",
        "project": "XCWarningsDemo",
        "count": 1
    }
]
```

## Running Tests

Once you have your `virtualenv` activated and all the dependencies installed, run the tests:

`python3 -m pytest`

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
