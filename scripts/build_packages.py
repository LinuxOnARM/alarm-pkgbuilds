# Import Statements
import utils.db as db
import utils.build as build

# File Docstring
# @LinuxOnARM || build_packages.py
# ---------------------------------------
# Builds packages that are marked "for build". Must be called
# AFTER prepare_packages.py
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

	# Instance a new Build system
	buildSystem: build.Build = build.Build()

	# Get a list of all packages
	allPackages: list[db.PackageInfo] = database.getAllPackages()

	# Counter
	currentPackageCount: int = 1
	allPackagesCount: int = len(allPackages)

	# Iterate through all packages
	for package in allPackages:
		# Log
		_printLog(currentPackageCount, allPackagesCount,
				  f"Checking build status for \"{package.getPackageName()}\" package...")

		# Check if package is marked for build
		if not package.getPackageBuildInfo().isMarkedForBuild():
			# Log
			_printLog(currentPackageCount, allPackagesCount,
					  f"Skipping \"{package.getPackageName()}\" || Not marked for build!")

			# Increment counter
			currentPackageCount += 1

			# Continue to next package
			continue

		# Log
		_printLog(currentPackageCount, allPackagesCount,
				  f"Executing build function...")

		# Execute
		try:
			buildSystem.buildPackage(package)
		except Exception as error:
			_printLog(currentPackageCount, allPackagesCount,
					  f"Error while building package || {error}")

		# Increment counter
		currentPackageCount += 1

# Public Methods

# Private Methods
def _printLog(counter: int, max: int, message: any) -> None:
	"""
	Prints to log a nicely formatted message

	@param { int } counter - The current counter value
	@param { int } max - The maximum amount of log messages
	@param { any | str } message - The message to output
	@return None
	"""
	print(f"[PKG BUILD][{counter}/{max}] {message}")

# Run
if __name__ == "__main__":
	main()