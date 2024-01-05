# Import Statements

# File Docstring
# @LinuxOnARM || logging.py
# ---------------------------------------
# Provides a simple to use logging system.
#
# Authors: @MaxineToTheStars <https://github.com/MaxineToTheStars>
#          @LinuxOnARM       <https://github.com/LinuxOnARM>
# ----------------------------------------------------------------

# Enums

# Interfaces

# Public Variables

# Private Variables

# Constants

# Public Methods
def log(logTitle: str, packageName: str, currentLogValue: int, maximumLogCount: int, message: str) -> int:
    """
    Prints a formatted message to the console.

    @param { str } logTitle - The title of the log
    @param { str } packageName - The name of the package
    @param { int } currentLogValue - The current count of the log
    @param { int } maximumLogCount - The maximum number of logs
    @param { str } message - The message to output
    @return { int } - The new current log value
    """
    # Log message to console
    print(
        f"[{logTitle} @ {packageName}][{currentLogValue}/{maximumLogCount}] {message}"
    )

    # Return new count
    return currentLogValue + 1

# Private Methods
