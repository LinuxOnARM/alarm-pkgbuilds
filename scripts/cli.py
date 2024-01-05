# Import Statements
# First party
from typing import Final

# Second party
import utils.db as db

# Third party

# File Docstring
# @LinuxOnARM || build_packages.py
# ---------------------------------------
# A CLI tool that allows for interacting with the database
#
# Authors: @MaxineToTheStars <https://github.com/MaxineToTheStars>
#          @LinuxOnARM       <https://github.com/LinuxOnARM>
# ----------------------------------------------------------------

# Class Definition
class Functions:
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables
    _db: Final[db.Database] = db.Database()

    # Constants

    # Constructor
    def __init__(self) -> None:
        return

    # Public Methods
    def get(self, inputs: list[str]) -> str:
        """
        Prints out all attached information about the specified package.

        @param { str } packageName - The name of the package in the database
        @return str - Package info
        """

        # Check if inputs are passed
        if len(inputs) == 0 or inputs[0] == "":
            # Handle case
            return "Missing parameters: { str } packageName - The name of the package in the database"

        # Get the package name input
        packageName: Final[str] = inputs[0]

        # Hold package data
        packageData: db.PackageInfo = None

        # Try to retrieve package data from database
        try:
            # Retrieve package data
            packageData = self._db.getPackage(packageName)
        except Exception:
            # Handle exception
            return "Function error: Package was not found"

        # Print package data
        print("Package Name: {a}".format(a=packageData.getPackageName()))
        print("Package Version: {a}".format(a=packageData.getPackageVersion()))
        print(
            "Package URLS:\n	Type: {a}\n	Source URL: {b}\n	Upstream URL: {c}".format(
                a=packageData.getPackageURLs().getSourceType(),
                b=packageData.getPackageURLs().getSourceURL(),
                c=packageData.getPackageURLs().getUpstreamURL(),
            )
        )
        print(
            "Package Paths:\n	Repo: {a}\n	PKGBUILD: {b}".format(
                a=packageData.getPackagePaths().getInternalRepositoryPath(),
                b=packageData.getPackagePaths().getPackageBuildPath(),
            )
        )
        print(
            "Package Build:\n	Marked For Build: {a}\n	Build Function Name: {b}\n	Prepare Function Name: {c}".format(
                a=packageData.getPackageBuildInfo().isMarkedForBuild(),
                b=packageData.getPackageBuildInfo().getPackageBuildFunctionName(),
                c=packageData.getPackageBuildInfo().getPackagePrepareFunctionName(),
            )
        )

        # Return
        return ""

    def new(self, inputs: list[str]) -> str:
        """
        Adds a new package to the package database

        @param { str } packageName - The name of the package
        @param { str } packageVersion - The version of the package
        @param { str } packageURLType - The URL type of the package's source
        @param { str } packageSourceURL - The URL of the package's source
        @param { str } packageUpstreamURL - The URL of the package's upstream source
        @param { str } packageRepository - Which repository is the package under
        @return str - New package info
        """
        # Import Statements
        import os
        from subprocess import call

        # Check if inputs are passed
        if len(inputs) == 0 or inputs[0] == "":
            # Handle case
            return "Missing parameters:\n   { str } packageName - The name of the package\n   { str } packageVersion - The version of the package\n   { str } packageURLType - The URL type of the package's source\n   { str } packageSourceURL - The URL of the package's source\n   { str } packageUpstreamURL - The URL of the package's upstream source\n   { str } packageRepository - Which repository is the package under"

        # Get the necessary inputs
        packageName: Final[str] = inputs[0]
        packageVersion: Final[str] = inputs[1]
        packageURLType: Final[str] = inputs[2]
        packageSourceURL: Final[str] = inputs[3]
        packageUpstreamURL: Final[str] = inputs[4]
        packageRepositoryPath: Final[str] = f"/aarch64/{inputs[5]}/os/{packageName}"
        packagePKGBUILDPath: Final[str] = f"/pkgbuild/{packageName}"

        # Generate directory paths
        repositoryPath: Final[str] = os.getcwd().replace(
            "/scripts", f"/packages/{inputs[5]}/os/aarch64/{packageName}"
        )
        pkgbuildPath: Final[str] = os.getcwd().replace(
            "/scripts", f"/pkgbuild/{packageName}"
        )

        # Create folders
        call(["mkdir", "--parents", repositoryPath])
        call(["mkdir", "--parents", pkgbuildPath])

        # PKGBUILD Template
        pkgbuildTemplate: Final[str] = f"# Package Information\n# ------------\n# PKGBUILD for {packageName} package\n#\n# Maintainer: Your Name <example@email.com>\n# ------------------------------------------------------------------\n"

        # Generate PKGBUILD
        pkgbuildFile = open(f"{pkgbuildPath}/PKGBUILD", "a+")
        pkgbuildFile.write(pkgbuildTemplate)
        pkgbuildFile.close()

        # Create .gitkeep file
        open(f"{repositoryPath}/.gitkeep", "a").close()

        # Try to create a new entry
        try:
            # Create a new entry
            self._db.addPackage(
                packageName,
                packageVersion,
                packageURLType,
                packageSourceURL,
                packageUpstreamURL,
                packageRepositoryPath,
                packagePKGBUILDPath,
            )
        except Exception:
            # Handle exception
            return "Function error: Database error"

        # Print out information
        self.get([packageName])

        # Return
        return ""

    def remove(self, inputs: list[str]) -> str:
        """
        Removes a given package from the database

        @param { str } packageName - The name of the package in the database
        @return str - Package info
        """
        # Import Statements
        from subprocess import call

        # Check if inputs are passed
        if len(inputs) == 0 or inputs[0] == "":
            # Handle case
            return "Missing parameters: { str } packageName - The name of the package in the database"

        # Get the package name input
        packageName: Final[str] = inputs[0]

        # Hold package data
        packageData: db.PackageInfo = None

        # Try to retrieve package data from database
        try:
            # Retrieve package data
            packageData = self._db.getPackage(packageName)
        except Exception:
            # Handle exception
            return "Function error: Package was not found"

        # Delete the package's file entries
        call(
            [
                "rm",
                "--recursive",
                "--force",
                packageData.getPackagePaths().getPackageBuildPath(),
            ]
        )
        call(
            [
                "rm",
                "--recursive",
                "--force",
                packageData.getPackagePaths().getInternalRepositoryPath(),
            ]
        )

        # Delete the package from the database
        self._db.deletePackage(packageName)

        # Log
        print(f'Package "{packageName}" was deleted!')

        # Return
        return ""

    # Private Methods

# Enums

# Interfaces

# Constants
__version___: Final[str] = "1.0.0"

# Public Variables

# Private Variables

# main()
def main() -> None:
    # Log
    print(f"CLI for ALARM Package Database || v{__version___}")
    print('Type "help" for help!')

    # Input Loop
    while True:
        # Retrieve raw input
        rawInput: str = input(":")

        # Clean input
        prompt: Final[str] = rawInput.lower()

        # Hold function data
        functionName: str = ""
        functionParameters: list[str] = [""]

        # Try to parse the prompt
        try:
            # Parse the prompt
            functionName = prompt.split("(", 1)[0]
            functionParameters = prompt.removesuffix(")").split("(", 1)[1].split(", ")
        except Exception:
            # Execution occurred, print out error
            print("Invalid command!")
            continue

        # Check if method exists
        if not hasattr(Functions, functionName):
            print("Invalid command!")
            continue

        # Get the specified command/function
        command = getattr(Functions(), functionName)

        # Execute with parameters
        print("\n----------")
        print(command(functionParameters))
        print("----------")

# Public Methods

# Private Methods

# Run
if __name__ == "__main__":
    main()
