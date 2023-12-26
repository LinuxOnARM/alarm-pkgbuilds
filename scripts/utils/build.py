# Import Statements
import utils.db as db
from typing import Final

# File Docstring
# @LinuxOnARM || build_packages.py
# ---------------------------------------
# Builds packages that are marked "for build". Must be called
# AFTER prepare_packages.py
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
		pass

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

		# Logging setup
		logCounter: int = 1
		numberOfLogs: Final[int] = 11
		currentPackageName: Final[str] = package.getPackageName()

		# Log
		logCounter = self._printLog(
			logCounter, numberOfLogs, currentPackageName, "Building package...")

		# Save current directory path
		rootDirectory: str = os.getcwd()

		# Switch directories
		os.chdir(package.getPackagePaths().getPackageBuildPath())

		# Run makepkg
		subprocess.call(["makepkg", "--sign"])

		# Switch directories
		os.chdir(rootDirectory)

		# Log
		logCounter = self._printLog(
			logCounter, numberOfLogs, currentPackageName, "Done!")

	# Private Methods
	def _printLog(self, counter: int, max: int, packageName: str, message: str) -> int:
		"""
		Prints to log a nicely formatted message

		@param { int } counter - The current counter value
		@param { int } max - The maximum amount of log messages
		@param { str } packageName - The name of the package
		@param { any | str } message - The message to output
		@return int - The new value of `counter`
		"""
		# Log
		print(f"[PKG BUILD][{packageName}][{counter}/{max}] {message}")

		# Return new counter value
		return counter + 1

class Build:
	# Enums

	# Interfaces

	# Public Variables

	# Private Variables

	# Constants

	# Constructor
	def __init__(self) -> None:
		pass

	# Public Methods
	def buildPackage(self, package: db.PackageInfo) -> None:
		"""
		Runs the package's build package function

		@param { PackageInfo } package - The package
		@return None
		"""
		# Check if valid build function
		if not self._isValidBuildFunction(package.getPackageBuildInfo().getPackageBuildFunctionName()):
			raise BuildFunctionNotFound(
				f"Build function for package \"{package.getPackageName()}\" was not found")

		# Get build function
		buildFunction = getattr(
			BuildFunctions(), package.getPackageBuildInfo().getPackageBuildFunctionName())

		# Run
		buildFunction(package)

	# Private Methods
	def _isValidBuildFunction(self, functionName: str) -> bool:
		"""
		Checks if a given build function is valid

		@param { str } functionName - The name of the function
		@return bool
		"""
		return hasattr(BuildFunctions, functionName)

# Run
if __name__ == "__main__":
	pass