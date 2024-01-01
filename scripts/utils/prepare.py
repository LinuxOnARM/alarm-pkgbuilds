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
        Preparation function for linux package

        @param { PackageInfo } package - The package
        @return None
        """
        # Import statements
        import os
        import tarfile
        import hashlib
        import subprocess
        from urllib.request import urlretrieve

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

        # Preparation directory setup
        rootDirectory: str = os.getcwd()
        preparationDirectory: str = "./temp"

        # Create preparation directory
        os.mkdir(preparationDirectory)

        # Switch directories
        os.chdir(preparationDirectory)

        # Retrieve version info
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

        # Format the download URL
        downloadURL: str = package.getPackageURLs().getSourceURL(
            [kernelMajorVersionNumber, kernelVersionNumber]
        )

        # Download the Kernel tarfile
        urlretrieve(downloadURL, f"linux-{kernelVersionNumber}.tar.xz")

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

        # Extract the Kernel
        kernelTarFile: tarfile.TarFile = tarfile.open(
            f"linux-{kernelVersionNumber}.tar.xz"
        )
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
        os.chdir(rootDirectory)

        # Copy the new configuration file to the Linux PKGBUILD directory
        subprocess.call(
            [
                "cp",
                "--recursive",
                "--update",
                "--verbose",
                f"{preparationDirectory}/linux-{kernelVersionNumber}/.config",
                f"{package.getPackagePaths().getPackageBuildPath()}/config",
            ]
        )

        # Generate new checksums
        newCheckSums: str = "{x} SKIP {x}"
        kernelTarFileCheckSum: str = ""
        kernelConfigurationFileChecksum: str = ""

        # Kernel checksum
        with open(
            f"{preparationDirectory}/linux-{kernelVersionNumber}.tar.xz", "rb"
        ) as kernelTarFile:
            kernelTarFileCheckSum = hashlib.sha256(kernelTarFile.read()).hexdigest()
            kernelTarFile.close()

        # Kernel configuration file checksum
        with open(
            f"{preparationDirectory}/linux-{kernelVersionNumber}/.config", "rb"
        ) as kerneConfigurationFile:
            kernelConfigurationFileChecksum = hashlib.sha256(
                kerneConfigurationFile.read()
            ).hexdigest()
            kerneConfigurationFile.close()

        # Edit the PKGBUILD
        self._pkgbuildModifyVersionKey(
            f"{package.getPackageVersion()}.aarch64",
            package.getPackagePaths().getPackageBuildPath(),
        )
        self._pkgbuildModifySha256CheckSumKey(
            newCheckSums.replace("{x}", kernelTarFileCheckSum, 1).replace(
                "{x}", kernelConfigurationFileChecksum, 1
            ),
            package.getPackagePaths().getPackageBuildPath(),
        )

        # Log
        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Cleaning up...",
        )

        # Delete the preparation directory
        subprocess.call(["rm", "--recursive", "--force", preparationDirectory])

        # Log
        currentLogCount = logging.log(
            "PREPARE",
            package.getPackageName(),
            currentLogCount,
            maximumLogCount,
            "Done!",
        )

    # Private Methods
    def _pkgbuildModifyVersionKey(self, newVersion: str, path: str) -> None:
        """
        Modifies the given PKGBUILD's version entry

        @param { str } newVersion - The new version of the package
        @param { str } path - The path to the PKGBUILD's directory
        @return None
        """
        # Sed command
        sedSyntax: Final[str] = f"s|^pkgver=.*|pkgver={newVersion}|g"

        # Execute sed
        os.system(f"sed --in-place '{sedSyntax}' {path}/PKGBUILD")

    def _pkgbuildModifySha256CheckSumKey(self, newCheckSum: str, path: str) -> None:
        """
        Modifies the given PKGBUILD's sha256 checksum entry

        @param { str } newCheckSum - The new checksum
        @param { str } path - The path to the PKGBUILD's directory
        @return None
        """
        # Sed command
        sedSyntax: Final[str] = f"s|^sha256sums=.*|sha256sums=( {newCheckSum} )|g"

        # Execute sed
        os.system(f"sed --in-place '{sedSyntax}' {path}/PKGBUILD")

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
        Runs the package's prepare package function

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
        Checks if a given prepare function is valid

        @param { str } functionName - The name of the function
        @return bool - Is a valid prepare function
        """
        return hasattr(PrepareBuildFunctions, functionName)

# Run
if __name__ == "__main__":
    pass
