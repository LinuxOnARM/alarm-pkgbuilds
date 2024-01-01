# Import Statements
# First party
from typing import Final

# Second party
import utils.db as db
import utils.logging as logging

# Third party

# File Docstring
# @LinuxOnARM || build_packages.py
# ---------------------------------------
# A series of building functions for building packages.
#
# Authors: @MaxineToTheStars <https://github.com/MaxineToTheStars>
#          @LinuxOnARM       <https://github.com/LinuxOnARM>
# ----------------------------------------------------------------

# Class Definitions
class BuildFunctionNotFound(Exception):
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables

    # Constants

    # Constructor
    def __init__(self, message: str) -> None:
        # Class base class constructor
        super().__init__(message)

    # Public Methods

    # Private Methods

class BuildFunctions:
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables

    # Constants

    # Constructor
    def __init__(self) -> None:
        return

    # Public Methods
    def build_pkg_linux(self, package: db.PackageInfo) -> None:
        """
        Build function for linux package

        @param { PackageInfo } package - The package
        @return None
        """
        # Import statements
        import os
        import subprocess

        # Setup logging
        maximumLogCount: Final[int] = 11
        currentLogCount: int = 1

        # Log
        currentLogCount = logging.log(
            "BUILD",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Building package...",
        )

        # Save current directory path
        rootDirectory: str = os.getcwd()

        # Switch directories
        os.chdir(package.getPackagePaths().getPackageBuildPath())

        # Run makepkg
        subprocess.call(["makepkg", "--sign"])

        # Switch directories
        os.chdir(rootDirectory)

        # Log
        currentLogCount = logging.log(
            "BUILD",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Done!",
        )

class Build:
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables

    # Constants

    # Constructor
    def __init__(self) -> None:
        return

    # Public Methods
    def buildPackage(self, package: db.PackageInfo) -> None:
        """
        Runs the package's build package function

        @param { PackageInfo } package - The package
        @return None
        """
        # Check if valid build function
        if not self._isValidBuildFunction(
            package.getPackageBuildInfo().getPackageBuildFunctionName()
        ):
            raise BuildFunctionNotFound(
                f'Build function for package "{package.getPackageName()}" was not found'
            )

        # Get build function
        buildFunction = getattr(
            BuildFunctions(),
            package.getPackageBuildInfo().getPackageBuildFunctionName(),
        )

        # Run
        buildFunction(package)

    # Private Methods
    def _isValidBuildFunction(self, functionName: str) -> bool:
        """
        Checks if a given build function is valid

        @param { str } functionName - The name of the function
        @return bool - Is a valid build function
        """
        return hasattr(BuildFunctions, functionName)

# Run
if __name__ == "__main__":
    pass
