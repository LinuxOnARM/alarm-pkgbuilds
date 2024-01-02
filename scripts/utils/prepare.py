# Import Statements
# First party
import os
from typing import Final

# Second party
import utils.db as db
import utils.logging as logging

# Third party

# File Docstring
# @LinuxOnARM || prepare.py
# ---------------------------------------
# A series of preparation functions for preparing packages.
#
# Authors: @MaxineToTheStars <https://github.com/MaxineToTheStars>
#          @LinuxOnARM       <https://github.com/LinuxOnARM>
# ----------------------------------------------------------------

# Class Definitions
class PrepareBuildFunctionNotFound(Exception):
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

class PrepareBuildFunctions:
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables

    # Constants

    # Constructor
    def __init__(self) -> None:
        return

    # Public Methods
    def prepare_pkg_linux(self, package: db.PackageInfo) -> None:
        """
        Preparation function for the `linux-aarch64` package.

        @param { PackageInfo } package - The package object
        @return None
        """
        # Import Statements
        import os, tarfile, subprocess

        # Setup logging
        maximumLogCount: Final[int] = 11
        currentLogCount: int = 1

        # Log
        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Starting package preparations...",
        )

        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Creating temporary directory...",
        )

        # Create temporary directory
        directories: Final[tuple[str, str]] = self._createTemporaryDirectory()

        # Retrieve Kernel version info
        kernelVersionNumber: str = package.getPackageVersion()
        kernelMajorVersionNumber: str = f"{kernelVersionNumber[0]}"

        # Log
        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Downloading Linux Kernel...",
        )

        # Retrieve a formatted download URL
        downloadURL: Final[str] = package.getPackageURLs().getSourceURL(
            [kernelMajorVersionNumber, kernelVersionNumber]
        )

        # Download the Kernel tarfile
        sourceFilePath: Final[str] = self._downloadSourceFiles(
            downloadURL, package.getPackageURLs().getSourceType()
        )

        # Log
        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Linux Kernel downloaded...",
        )

        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Extracting Linux Kernel...",
        )

        # Extract the Linux Kernel
        kernelTarFile: tarfile.TarFile = tarfile.open(sourceFilePath)
        kernelTarFile.extractall(".")
        kernelTarFile.close()

        # Log
        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Linux Kernel extracted...",
        )

        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Generating Kernel configuration file for AArch64...",
        )

        # Switch directories
        os.chdir(f"linux-{kernelVersionNumber}")

        # Generate a new Kernel configuration file
        subprocess.call(["make", "ARCH=arm64", "defconfig"])

        # Log
        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Kernel configuration file generated...",
        )

        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Modifying PKGBUILD...",
        )

        # Switch directories
        os.chdir(directories[0])

        # Copy the new configuration file to the Linux PKGBUILD directory
        subprocess.call(
            [
                "cp",
                "--recursive",
                "--update",
                "--verbose",
                f"{directories[1]}/linux-{kernelVersionNumber}/.config",
                f"{package.getPackagePaths().getPackageBuildPath()}/config",
            ]
        )

        # Generate new SHA256 checksums
        newSHA256Checksums: Final[str] = self._generateSHA256Checksums(
            "{X} SKIP {X}",
            sourceFilePath,
            f"{directories[1]}/linux-{kernelVersionNumber}/.config",
        )

        # Modify the PKGBUILD version entry
        self._modifyVersionPKGBUILDEntry(
            package.getPackagePaths().getPackageBuildPath(),
            f"{kernelVersionNumber}.aarch64",
        )

        # Modify the PKGBUILD sha256 entry
        self._modifySHA256PKGBUILDEntry(
            package.getPackagePaths().getPackageBuildPath(), newSHA256Checksums
        )

        # Log
        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Cleaning up...",
        )

        # Delete the temporary directory
        subprocess.call(["rm", "--recursive", "--force", directories[1]])

        # Log
        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Done!",
        )

    # Private Methods
    def _createTemporaryDirectory(self) -> tuple[str, str]:
        """
        Creates a new, temporary directory, for package preparation.

        @return tuple(str, str) - Old directory path, Temporary directory path
        """
        # Get current directory
        currentOldDirectory: Final[str] = os.getcwd()

        # Temporary directory name
        temporaryDirectory: Final[str] = "./temp"

        # Create temporary directory
        os.mkdir(temporaryDirectory)

        # Switch directories
        os.chdir(temporaryDirectory)

        # Return
        return (currentOldDirectory, os.getcwd())

    def _downloadSourceFiles(self, downloadURL: str, urlType: str) -> str:
        """
        Downloads the given source file(s) via `https` or `git+https`.

        @param { str } downloadURL - The download URL
        @param { str } urlType - The type of the download URL
        @return str - Filepath to the source download
        """
        # Import Statements
        from subprocess import call
        from urllib.request import urlretrieve

        # HTTP(S) download
        if urlType == "http":
            # Download
            return urlretrieve(downloadURL)[0]

        # Git download
        elif urlType == "git+http":
            # Git clone
            call(["git", "clone", downloadURL])

        # Invalid params
        else:
            raise Exception("Invalid download URL or URL type")

    def _generateSHA256Checksums(self, format: str, *files: str) -> str:
        """
        Generates SHA256 checksums based on the given files.

        @param { str } format - Format string
        @param { str } files - Filepaths to the given file(s)
        @return str - The new generated checksums
        """
        # Import Statements
        import hashlib

        # Template
        templateEntry: str = f"sha256sums=( {format} )"

        # Iterate through each file and generate the checksum
        for file in files:
            with open(file, "rb") as file:
                templateEntry = templateEntry.replace(
                    "{X}", hashlib.sha256(file.read()).hexdigest(), 1
                )
                file.close()

        # Return new checksums
        return templateEntry

    def _modifySHA256PKGBUILDEntry(self, directoryPath: str, value: str) -> None:
        """
        Modifies the given PKGBUILD's sha256 checksum entry.

        @param { str } directoryPath - The path to the directory with the PKGBUILD
        @param { str } value - The new checksum value
        @return None
        """
        # Import Statements
        from subprocess import call

        # Sed command
        sedSyntax: Final[str] = f"s|^sha256sums=.*|{value}|g"

        # Execute sed
        call(["sed", "--in-place", sedSyntax, f"{directoryPath}/PKGBUILD"])

    def _modifyVersionPKGBUILDEntry(self, directoryPath: str, value: str) -> None:
        """
        Modifies the given PKGBUILD's version entry.

        @param { str } directoryPath - The path to the directory with the PKGBUILD
        @param { str } value - The new version value
        @return None
        """
        # Import Statements
        from subprocess import call

        # Sed command
        sedSyntax: Final[str] = f"s|^pkgver=.*|pkgver={value}|g"

        # Execute sed
        call(["sed", "--in-place", sedSyntax, f"{directoryPath}/PKGBUILD"])

class PrepareBuild:
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables

    # Constants

    # Constructor
    def __init__(self) -> None:
        pass

    # Public Methods
    def preparePackage(self, package: db.PackageInfo) -> None:
        """
        Runs the package's prepare package function.

        @param { PackageInfo } package - The package
        @return None
        """
        # Check if valid prepare function
        if not self._isValidPrepareFunction(
            package.getPackageBuildInfo().getPackagePrepareFunctionName()
        ):
            raise PrepareBuildFunctionNotFound(
                f'Prepare function for package "{package.getPackageName()}" was not found'
            )

        # Get prepare function
        prepareBuildFunction = getattr(
            PrepareBuildFunctions(),
            package.getPackageBuildInfo().getPackagePrepareFunctionName(),
        )

        # Run
        prepareBuildFunction(package)

    # Private Methods
    def _isValidPrepareFunction(self, functionName: str) -> bool:
        """
        Checks if a given prepare function is valid.

        @param { str } functionName - The name of the function
        @return bool - Is a valid prepare function
        """
        return hasattr(PrepareBuildFunctions, functionName)

# Run
if __name__ == "__main__":
    pass
