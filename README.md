# Arch Linux on ARM (ALARM) || Automated PKGBUILDs
A GitHub repository that automates the process of updating and building packages for Arch Linux on the AArch64 architecture

## Usage
TBA

## How It Works
The following sections detail how the automation and building process occur. The `Synopsis` header in each section give a Tl;DR "overview"

<details>

<!-- Section Title -->
<summary> 0. Storing Packages and their Data </summary>

<!-- Header -->
#### JSON to the Rescue!
---
While this project is intended to be autonomous there still has to be a human to upload and configure their package's information and PKGBUILD on this repository. That's were [db.py][db-python-linkage] and [db.json][db-json-linkage] come in. The `Database` class (aka: [db.py][db-python-linkage]) provides an easy to use JSON wrapper for modifying data in [db.json][db-json-linkage]. The actual "Database" (aka [db.json][db-json-linkage]) is a easy to read JSON file that specifies just enough information needed to sync, prepare, and build a given package. It is considered the core to the automation process.

#### Synopsis
---
Using the power of JSON and Python classes a simple to use API can be used to modify and add packages for automated syncing and building.

</details>

<!-- Separator -->

<details>

<!-- Section Title -->
<summary> 1. Pulling Upstream Package Data from Mainline Arch Linux </summary>

<!-- Header -->
#### Using the Arch Linux Package List to Our Advantage
---
The Arch Linux package search provides a easy to use way of looking up, flagging, and downloading snapshots of packages. Users can _mark_ a certain package or packages as outdated notifying the maintainer to update the PKGBUILD and schedule a rebuild. After a package has been updated the new package information is shows on the package's webpage. In order to _sync-up_ with mainstream Arch Linux the Python script [sync_package_database.py][sync-package-database-python-linkage] compares the version number of the currently builded package and the package shows in the Arch Linux package search. If a version mismatch is found it modifies the package's database entry changing the version number and marking it for build.

#### Synopsis
---
Using the power of free labor and a fancy Python script you can kick back and let the code do all the magic!

</details>

<!-- Separator -->

<details>

<!-- Section Title -->
<summary> 2. Preparing Packages for Building </summary>

<!-- Header -->
#### Manual Intervention Required
---
Due to how every package is different I couldn't really implement a "universal packaging system". This is due to packages requiring different dependencies and each package needing their own checksums and what not. However, a crude but simple to use system is available for preparing packages for building. While very early in its stage given some time to mature it could achieve a sort of "universal" status to it. Refer to [prepare.py][prepare-python-linkage] and [prepare_packages.py][prepare-packages-python-linkage] for more information and code.

#### Synopsis
---
MFW you have to write a bit of code for this :(

</details>

<!-- Separator -->

<details>

<!-- Section Title -->
<summary> 3. Building Packages </summary>

<!-- Header -->
#### The Fun Part
---
TBA (currently in work)

#### Synopsis
---
TBA (currently in work)

</details>

<!-- Links -->
[db-python-linkage]: ./scripts/utils/db.py
[db-json-linkage]: ./scripts/db/db.json
[sync-package-database-python-linkage]: ./scripts/sync_package_database.py
[prepare-python-linkage]: ./scripts/utils/prepare.py
[prepare-packages-python-linkage]: ./scripts/prepare_packages.py
