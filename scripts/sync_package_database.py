# Import Statements
# First party
import re
from typing import Final
from urllib import request
from subprocess import call

# Second party
import utils.db as db
import utils.logging as logging

# Third party
from bs4 import BeautifulSoup

# File Docstring
# @LinuxOnARM || sync_package_database.py
# ---------------------------------------
# Makes a series of HTTP(S) calls to the Arch Linux
# package search database and pulls the latest version
# info of available packages.
#
# Authors: @MaxineToTheStars <https://github.com/MaxineToTheStars>
#          @LinuxOnARM       <https://github.com/LinuxOnARM>
# ----------------------------------------------------------------

# Enums

# Interfaces

# Constants
FILTERED_WORDS: Final[list[str]] = [".arch1-1"]
FIND_VERSION_ENTRY_REGEX_PATTERN: Final[str] = r'content="[^"]*"'

# Public Variables

# Private Variables

# main()
def main() -> None:
    # Instance a new Database
    database: db.Database = db.Database()

    # Get a list of all packages
    allPackages: Final[list[db.PackageInfo]] = database.getAllPackages()

    # Setup logging
    maximumLogCount: Final[int] = len(allPackages) + 1
    currentLogCount: int = 1

    # Create a backup of the current database file
    call(["cp", "./db/db.json", "./db/db.old.json"])

    # Iterate through all packages
    for package in allPackages:
        # Check for the example package
        if package.getPackageName() == "example-package":
            # Skip the example package
            continue

        # Log
        currentLogCount = logging.log(
            "PACKAGE SYNC",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Pulling package info...",
        )

        # Get the upstream URL
        upstreamURL: str = package.getPackageURLs().getUpstreamURL()

        # Download the HTML
        pkgDataRaw = request.urlopen(upstreamURL).read().decode("utf-8")

        # Parse the HTML
        pkgDataClean = BeautifulSoup(pkgDataRaw, "html.parser")

        # Find the package version
        pkgVersionRaw = (
            pkgDataClean.find(id="pkgdetails")
            .find(itemprop="version")
            .decode(None, "utf-8")
        )

        # Check if a string was returned
        if pkgVersionRaw == None or not pkgVersionRaw is str:
            # Move on to the next package
            continue

        # Clean the version data
        pkgVersionClean: str = _cleanVersionString(pkgVersionRaw)

        # Compare the version numbers
        if package.getPackageVersion() == pkgVersionClean:
            # Mark for "Do Not Build"
            database.modifyPackage(
                package.getPackageName(), "buildInfo/markedForBuild", False
            )

            # Log
            currentLogCount = logging.log(
                "PACKAGE SYNC",
                package.getPackageName(),
                currentLogCount,
                maximumLogCount,
                f'Marked for "Do not Build" || Current Version: v{package.getPackageVersion()}',
            )
        else:
            # Store the old version for logging
            oldPackageVersion: str = package.getPackageVersion()

            # Mark for "Do Build"
            database.modifyPackage(
                package.getPackageName(), "buildInfo/markedForBuild", True
            )

            # Update the package version
            database.modifyPackage(package.getPackageName(), "version", pkgVersionClean)

            # Log
            currentLogCount = logging.log(
                "PACKAGE SYNC",
                package.getPackageName(),
                currentLogCount,
                maximumLogCount,
                f'Marked for "Build" || v{oldPackageVersion} -> v{package.getPackageVersion()}',
            )

# Public Methods

# Private Methods
def _cleanVersionString(rawVersionString: str) -> str:
    """
    Returns a clean version string.

    @param { str } rawVersionString - The raw version string
    @return str - A clean version string
    """
    # Output
    out: str = ""

    # Parse with RegEx
    compiledPattern: re.Pattern = re.compile(
        FIND_VERSION_ENTRY_REGEX_PATTERN, re.IGNORECASE
    )
    out = (
        compiledPattern.findall(rawVersionString)[0]
        .replace('content="', "")
        .replace('"', "")
    )

    # Remove filtered words
    for word in FILTERED_WORDS:
        out = out.replace(word, "")

    # Return
    return out

# Run
if __name__ == "__main__":
    main()
