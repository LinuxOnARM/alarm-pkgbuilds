# Import Statements
# First party
import os
import json
from typing import Final

# Second party

# Third party

# File Docstring
# @LinuxOnARM || db.py
# ---------------------------------------
# Loads the db.json file into memory and provides
# methods to modify and read data.
#
# Authors: @MaxineToTheStars <https://github.com/MaxineToTheStars>
#          @LinuxOnARM       <https://github.com/LinuxOnARM>
# ----------------------------------------------------------------

# Class Definitions
class PackageURLInfo:
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables
    _rawPackageURLInformation: dict

    # Constants

    # Constructor
    def __init__(self, rawPackageURLInfo: dict) -> None:
        # Set the package information
        self._rawPackageURLInformation = rawPackageURLInfo

    # Public Methods
    def getSourceURL(self, replacementList: list[str] = None) -> str:
        """
        Returns the URL of the package's source code.

        @param { list[str] } replacementList - A string list to be used for formatting (Optional)
        @return str - The source URL
        """
        # No replacement list provided, return raw source url
        if not replacementList:
            return self._rawPackageURLInformation["source_url"]

        # Output URL
        formattedURL: str = self._rawPackageURLInformation["source_url"]

        # Iterate through each word in replacement list
        for word in replacementList:
            formattedURL = formattedURL.replace("{x}", word, 1)

        # Return
        return formattedURL

    def getSourceType(self) -> str:
        """
        Returns the type of the source URL.

        @return str - The source type
        """
        return self._rawPackageURLInformation["type"]

    def getUpstreamURL(self) -> str:
        """
        Returns the URL of the package's upstream source.

        @return str - The upstream URL
        """
        return self._rawPackageURLInformation["upstream_url"]

    # Private Methods

class PackagePathInfo:
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables
    _rawPackagePathInformation: dict

    # Constants

    # Constructor
    def __init__(self, rawPackagePathInfo: dict) -> None:
        # Set the package information
        self._rawPackagePathInformation = rawPackagePathInfo

    # Public Methods
    def getPackageBuildPath(self) -> str:
        """
        Returns the absolute path to the package's PKGBUILD directory.

        @return str - The absolute path to the package's PKGBUILD directory
        """
        return os.getcwd().replace(
            "/scripts", self._rawPackagePathInformation["pkgbuild"]
        )

    def getInternalRepositoryPath(self) -> str:
        """
        Returns the absolute path to the package's repository directory.

        @return str - The absolute path to the package's repository directory
        """
        return os.getcwd().replace("/scripts", self._rawPackagePathInformation["repo"])

    # Private Methods

class PackageBuildInfo:
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables
    _rawPackageBuildInformation: dict

    # Constants

    # Constructor
    def __init__(self, rawPackageBuildInfo: dict) -> None:
        # Set the package information
        self._rawPackageBuildInformation = rawPackageBuildInfo

    # Public Methods
    def isMarkedForBuild(self) -> bool:
        """
        Returns if the package is marked for build.

        @return bool - Build status
        """
        return self._rawPackageBuildInformation["markedForBuild"]

    def getPackageBuildFunctionName(self) -> str:
        """
        Returns the build function name of the package.

        @return str - Build function name
        """
        return self._rawPackageBuildInformation["buildFunctionName"]

    def getPackagePrepareFunctionName(self) -> str:
        """
        Returns the prepare function name of the package.

        @return str - Prepare function name
        """
        return self._rawPackageBuildInformation["prepareFunctionName"]

    # Private Methods

class PackageInfo:
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables
    _rawPackageInformation: dict
    _packageName: str

    # Constants

    # Constructor
    def __init__(self, rawPackageInfo: dict, packageName: str) -> None:
        # Set the package information
        self._rawPackageInformation = rawPackageInfo
        self._packageName = packageName

    # Public Methods
    def getPackageVersion(self) -> str:
        """
        Returns the version number of the package.

        @return str - Package's version number
        """
        return self._rawPackageInformation["version"]

    def getPackageURLs(self) -> PackageURLInfo:
        """
        Returns the associated URL info of the package.

        @return PackageURLInfo - See PackageURLInfo
        """
        return PackageURLInfo(self._rawPackageInformation["urls"])

    def getPackagePaths(self) -> PackagePathInfo:
        """
        Returns the associated filepath info of the package.

        @return PackagePathInfo - See PackagePathInfo
        """
        return PackagePathInfo(self._rawPackageInformation["paths"])

    def getPackageBuildInfo(self) -> PackageBuildInfo:
        """
        Returns the associated build info of the package.

        @return PackageBuildInfo - See PackageBuildInfo
        """
        return PackageBuildInfo(self._rawPackageInformation["buildInfo"])

    def getPackageName(self) -> str:
        """
        Returns the name of the package.

        @return str - Name of the package
        """
        return self._packageName

    # Private Methods

class PackageNotFoundException(Exception):
    # Enums

    # Interfaces

    # Public Variables
    requestedPackage: str

    # Private Variables

    # Constants

    # Constructor
    def __init__(self, message: str, package: str) -> None:
        # Class base class constructor
        super().__init__(message)

        # Set the requested not found package
        self.requestedPackage = package

    # Public Methods

    # Private Methods

class Database:
    # Enums

    # Interfaces

    # Public Variables

    # Private Variables
    _storedJSONDatabase: any

    # Constants
    DATABASE_FILE_PATH: Final[str] = f"{os.getcwd()}/db/db.json"

    # Constructor
    def __init__(self) -> None:
        # Open the database in "read-binary" mode
        with open(self.DATABASE_FILE_PATH, "rb") as databaseFile:
            # Load the database into memory
            self._storedJSONDatabase = json.loads(databaseFile.read())
            # Close the database file
            databaseFile.close()

    # Public Methods
    def getPackage(self, packageName: str) -> PackageInfo:
        """
        Retrieves the given package information from the database.

        @param { str } packageName - The name of the package
        @return PackageInfo - See PackageInfo
        """
        # Get the list of available packages
        packageList: list[str] = self._storedJSONDatabase["packages"]

        # Check if package exists
        if packageName not in packageList:
            raise PackageNotFoundException(
                f'Package "{packageName}" was not found', packageName
            )

        # Package exists
        return PackageInfo(
            self._storedJSONDatabase["package_info"][packageName], packageName
        )

    def getAllPackages(self) -> list[PackageInfo]:
        """
        Returns a list with all available packages.

        @return list[Package] - A list of all available packages
        """
        # Get the list of available packages
        packageList: list[str] = self._storedJSONDatabase["packages"]

        # Output list
        out: list[PackageInfo] = []

        # Iterate through each package
        for package in packageList:
            # Append the package info to the output list
            out.append(
                PackageInfo(self._storedJSONDatabase["package_info"][package], package)
            )

        # Return the output
        return out

    def modifyPackage(self, packageName: str, keyPath: str, newValue: str) -> None:
        """
        Modifies a given package's information on the database.

        @param { str } packageName - The name of the package
        @param { str } keyPath - The key to modify
        @param { str } newValue - The new value of the key
        @return None
        """
        # Get the list of available packages
        packageList: list[str] = self._storedJSONDatabase["packages"]

        # Check if package exists
        if packageName not in packageList:
            raise PackageNotFoundException(
                f'Package "{packageName}" was not found', packageName
            )

        # Get the package info
        rawPackageInfo: dict = self._storedJSONDatabase["package_info"][packageName]

        # Split the key value
        splitKeyPath: list[str] = keyPath.split("/")

        # Check the depth
        if len(splitKeyPath) == 1:
            rawPackageInfo[splitKeyPath[0]] = newValue
        else:
            rawPackageInfo[splitKeyPath[0]][splitKeyPath[1]] = newValue

        # Write to database
        with open(self.DATABASE_FILE_PATH, "w") as databaseFile:
            # Write the database to file
            json.dump(self._storedJSONDatabase, databaseFile)
            # Close the database file
            databaseFile.close()

    def addPackage(self, packageName: str, packageVersion: str, packageURLType: str, packageSourceURL: str, packageUpstreamURL: str, packageRepo: str, packagePackageBuild: str) -> None:
        """
        Adds a new package to the package database.

        @param { str } packageName - The name of the package
        @param { str } packageVersion -  The version of the package
        @param { str } packageURLType - The URL type of the package's source
        @param { str } packageSourceURL - The URL of the package's source
        @param { str } packageUpstreamURL -  The URL of the package's upstream source
        @param { str } packageRepo - The package's internal repo location
        @param { str } packagePackageBuild -  The package's PKGBUILD location
        @return None
        """

        # Get the list of available packages
        packageList: list[str] = self._storedJSONDatabase["packages"]

        # Check if duplicate entry
        if packageName in packageList:
            raise Exception("Duplicate package entry")

        # Create function templates
        buildPackageTemplate: str = f"build_pkg_{packageName}".replace("-", "_")
        preparePackageTemplate: str = f"prepare_pkg_{packageName}".replace("-", "_")

        # Add new entry to packages array
        self._storedJSONDatabase["packages"].append(packageName)

        # Populate package_info dict
        self._storedJSONDatabase["package_info"][packageName] = {}
        self._storedJSONDatabase["package_info"][packageName]["version"] = packageVersion
        self._storedJSONDatabase["package_info"][packageName]["urls"] = {}
        self._storedJSONDatabase["package_info"][packageName]["urls"]["type"] = packageURLType
        self._storedJSONDatabase["package_info"][packageName]["urls"]["source_url"] = packageSourceURL
        self._storedJSONDatabase["package_info"][packageName]["urls"]["upstream_url"] = packageUpstreamURL
        self._storedJSONDatabase["package_info"][packageName]["paths"] = {}
        self._storedJSONDatabase["package_info"][packageName]["paths"]["repo"] = packageRepo
        self._storedJSONDatabase["package_info"][packageName]["paths"]["pkgbuild"] = packagePackageBuild
        self._storedJSONDatabase["package_info"][packageName]["buildInfo"] = {}
        self._storedJSONDatabase["package_info"][packageName]["buildInfo"]["markedForBuild"] = True
        self._storedJSONDatabase["package_info"][packageName]["buildInfo"]["buildFunctionName"] = buildPackageTemplate
        self._storedJSONDatabase["package_info"][packageName]["buildInfo"]["prepareFunctionName"] = preparePackageTemplate

        # Write to database
        with open(self.DATABASE_FILE_PATH, "w") as databaseFile:
            # Write the database to file
            json.dump(self._storedJSONDatabase, databaseFile)
            # Close the database file
            databaseFile.close()

    def deletePackage(self, packageName: str) -> None:
        """
        Deletes a given package from the database.

        @param { str } packageName - The name of the package
        @return None
        """
        # Get the list of available packages
        packageList: list[str] = self._storedJSONDatabase["packages"]

        # Check if package exists
        if packageName not in packageList:
            raise PackageNotFoundException(
                f'Package "{packageName}" was not found', packageName
            )

        # Remove from package array
        self._storedJSONDatabase["packages"].remove(packageName)

        # Remove from package_info dict
        self._storedJSONDatabase["package_info"].pop(packageName)

        # Write to database
        with open(self.DATABASE_FILE_PATH, "w") as databaseFile:
            # Write the database to file
            json.dump(self._storedJSONDatabase, databaseFile)
            # Close the database file
            databaseFile.close()

    # Private Methods

# Run
if __name__ == "__main__":
    # Database sanity checks
    # Debugging
    os._exit(1)

    # Create a new Database object
    database: Database = Database()

    # Fetch an invalid package
    try:
        database.getPackage("invalidPackage")
    except PackageNotFoundException as error:
        print("Package not found: " + error.requestedPackage)

    # Separator
    print("\n---\n")

    # Fetch a valid package and test all key paths
    linuxPackage: PackageInfo = database.getPackage("linux")
    print("Package Selected: linux")
    print("Package Version: " + linuxPackage.getPackageVersion())
    print(
        "Package URLS:\n	Type: {a}\n	Source URL: {b}\n	Upstream URL: {c}".format(
            a=linuxPackage.getPackageURLs().getSourceType(),
            b=linuxPackage.getPackageURLs().getSourceURL(),
            c=linuxPackage.getPackageURLs().getUpstreamURL(),
        )
    )
    print(
        "Package Paths:\n	Repo: {a}\n	PKGBUILD: {b}".format(
            a=linuxPackage.getPackagePaths().getInternalRepositoryPath(),
            b=linuxPackage.getPackagePaths().getPackageBuildPath(),
        )
    )
    print(
        "Package Build:\n	Marked For Build: {a}\n	Build Function Name: {b}\n	Prepare Function Name: {c}".format(
            a=linuxPackage.getPackageBuildInfo().isMarkedForBuild(),
            b=linuxPackage.getPackageBuildInfo().getPackageBuildFunctionName(),
            c=linuxPackage.getPackageBuildInfo().getPackagePrepareFunctionName(),
        )
    )

    # Debugging
    os._exit(1)

    # Add a new package
    database.addPackage(
        "testing",
        "1.0.0",
        "https",
        "https://www.google.com",
        "https://www.google.com",
        "/aarch64/core/os",
        "/pkgbuild/google",
    )

    # Debugging
    os._exit(1)

    # Separator
    print("\n---\n")

    # Fetch a valid package and test all key paths
    testingPackage: PackageInfo = database.getPackage("testing")
    print("Package Selected: testing")
    print("Package Version: " + testingPackage.getPackageVersion())
    print(
        "Package URLS:\n	Type: {a}\n	Source URL: {b}\n	Upstream URL: {c}".format(
            a=testingPackage.getPackageURLs().getSourceType(),
            b=testingPackage.getPackageURLs().getSourceURL(),
            c=testingPackage.getPackageURLs().getUpstreamURL(),
        )
    )
    print(
        "Package Paths:\n	Repo: {a}\n	PKGBUILD: {b}".format(
            a=testingPackage.getPackagePaths().getInternalRepositoryPath(),
            b=testingPackage.getPackagePaths().getPackageBuildPath(),
        )
    )
    print(
        "Package Build:\n	Marked For Build: {a}\n	Build Function Name: {b}\n	Prepare Function Name: {c}".format(
            a=testingPackage.getPackageBuildInfo().isMarkedForBuild(),
            b=testingPackage.getPackageBuildInfo().getPackageBuildFunctionName(),
            c=testingPackage.getPackageBuildInfo().getPackagePrepareFunctionName(),
        )
    )

    # Delete package
    database.deletePackage("testing")

    # Separator
    print("\n---\n")

    # Fetch an invalid package
    try:
        database.getPackage("testing")
    except PackageNotFoundException as error:
        print("Package not found: " + error.requestedPackage)
