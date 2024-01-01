# Import Statements
# First party
from typing import Final

# Second party
import utils.db as db
import utils.prepare as prepare
import utils.logging as logging

# Third party

# File Docstring
# @LinuxOnARM || prepare_packages.py
# ---------------------------------------
# Prepares packages marked for "build". Due
# to each package having a separate build process,
# it is recommended to have a separate prepare method for each
# package.
#
# Authors: @MaxineToTheStars <https://github.com/MaxineToTheStars>
#          @LinuxOnARM       <https://github.com/LinuxOnARM>
# ----------------------------------------------------------------

# Enums

# Interfaces

# Constants

# Public Variables

# Private Variables

# main()
def main() -> None:
    # Instance a new Database
    database: db.Database = db.Database()

    # Instance a new Prepare system
    prepareSystem: prepare.PrepareBuild = prepare.PrepareBuild()

    # Get a list of all packages
    allPackages: Final[list[db.PackageInfo]] = database.getAllPackages()

    # Setup logging
    maximumLogCount: Final[int] = len(allPackages) + 1
    currentLogCount: int = 1

    # Iterate through all packages
    for package in allPackages:
        # Log
        currentLogCount = logging.log(
            "PACKAGE PREPARATION",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Checking build info...",
        )

        # Check if package is marked for build
        if not package.getPackageBuildInfo().isMarkedForBuild():
            # Log
            currentLogCount = logging.log(
                "PACKAGE PREPARATION",
                package.getPackageName(),
                currentLogCount,
                maximumLogCount,
                "Skipping package || Not marked for build!...",
            )

            # Continue to the next package
            continue

        # Log
        currentLogCount = logging.log(
            "PACKAGE PREPARATION",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Executing prepare function...",
        )

        try:
            # Execute
            prepareSystem.preparePackage(package)
        except Exception as error:
            # Log
            currentLogCount = logging.log(
                "PACKAGE PREPARATION",
                package.getPackageName(),
                currentLogCount,
                maximumLogCount,
                f"Error while preparing package! || {error}",
            )

# Public Methods

# Private Methods

# Run
if __name__ == "__main__":
    main()
