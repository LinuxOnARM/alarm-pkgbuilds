# Import Statements
import re
import utils.db as db
from typing import Final
from urllib import request
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
VERSION_REGEX_PATTERN: Final[str] = r'content="[^"]*"'
FILTERED_WORDS: Final[list[str]] = [".arch1-1"]

# Public Variables

# Private Variables

# main()
def main() -> None:
	# Instance a new Database
	database: db.Database = db.Database()

	# Get a list of all packages
	allPackages: list[db.PackageInfo] = database.getAllPackages()

	# Counter
	currentPackageCount: int = 1
	allPackagesCount: int = len(allPackages)

	# Iterate through all packages
	for package in allPackages:
		# Log
		_printLog(
			currentPackageCount,
			allPackagesCount,
			f'Pulling package info for "{package.getPackageName()}"',
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

		# Clean the version data
		pkgVersionClean: str = _cleanVersionString(pkgVersionRaw)

		# Compare the version numbers
		if package.getPackageVersion() == pkgVersionClean:
			# Mark for "Do Not Build"
			database.modifyPackage(
				package.getPackageName(), "buildInfo/markedForBuild", False
			)

			# Log
			_printLog(
				currentPackageCount,
				allPackagesCount,
				f'Marked "{package.getPackageName()}" for "Do Not Build" || Pinned at v{package.getPackageVersion()}',
			)
		else:
			# Store the old version for logging
			oldPackageVersion: str = package.getPackageVersion()

			# Mark for "Do Build"
			database.modifyPackage(
				package.getPackageName(), "buildInfo/markedForBuild", True
			)
			# Update the package version
			database.modifyPackage(
				package.getPackageName(), "version", pkgVersionClean)

			# Log
			_printLog(
				currentPackageCount,
				allPackagesCount,
				f'Marked "{package.getPackageName()}" for "Do Build" || v{oldPackageVersion} -> {pkgVersionClean}',
			)

		# Increase the counter
		currentPackageCount += 1

# Public Methods

# Private Methods
def _printLog(counter: int, max: int, message: str) -> None:
	"""
	Prints to log a nicely formatted message

	@param { int } counter - The current counter value
	@param { int } max - The maximum amount of log messages
	@param { any | str } message - The message to output
	@return None
	"""
	# Log
	print(f"[PKG SYNC][{counter}/{max}] {message}")

def _cleanVersionString(rawVersionString: str) -> str:
	"""
	Returns a clean version string

	@param { str } rawVersionString - The raw version string
	@return str - A clean version string
	"""
	# Output
	out: str = ""

	# Parse with RegEx
	compiledPattern: re.Pattern = re.compile(
		VERSION_REGEX_PATTERN, re.IGNORECASE)
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