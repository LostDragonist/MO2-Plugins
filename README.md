## **Description**

This is a collection of [Mod Organizer 2 (MO2)](https://www.nexusmods.com/skyrimspecialedition/mods/6194)﻿ plugins created by me, LostDragonist! These are plugins that, for some reason or another, aren't included in the main release of MO2.

See mirrors section for Github link.

## **Included Plugins**

## **Conflict Deleter** (ConflictDeleter.py, LostDragonist-MO2-Plugins.zip)

Adds an option to the tools menu called "Conflict Deleter". This will iterate through all enabled mods and find files that are overwritten by other mods. Those files are then moved to a new backup mod, effectively removing them from the install. This is intended to improve performance of MO2 and the game after a mod list is considered finished. This should be considered a highly destructive tool and handled with care.

## **DumpMappings** (DumpMappings.py, LostDragonist-MO2-Plugins.zip)

Disabled by default. Generates a text file in the overwrite mod after running an executable in MO2. This file contains all the valid USVFS mappings as of when the executable was closed. Very useful when debugging USVFS or random plugin bugs.

## **Fix Game Registry Key** (FixGameRegKey.py, LostDragonist-MO2-Plugins.zip)

When running an application in MO2, this will check to make sure the registry key is correct according to the game being managed by MO2. This is useful when you have moved the game, when you've validated a game with Steam, when the game has updated, or if you have multiple installations of the game with different MO2 instances pointing to different installs.

Whenever the registry needs to be changed, a User Account Control (UAC) prompt may show up from the Registry Console Tool. You need to accept this for the change to occur!

For what it's worth, this functionality requires Powershell to be installed. Any modern Windows PC should have Powershell.

## **Game Redirector** (GameRedirector.py, LostDragonist-MO2-Plugins.zip)

Disabled by default. This plugin maps certain game files for some games to the game files used by other games. This is useful when mods/installers/tools are *technically* compatible with multiple games but may not be updated or might have some issues.

The currently supported game redirections are:

* Skyrim -> Enderal
* Skyrim -> Skyrim SE
* Skyrim SE -> Skyrim VR

The currently redirected files are:

* %LocalAppData%\<game>\plugins.txt
* %LocalAppData%\<game>\loadorder.txt
* My Games\<game>\<game>.ini
* My Games\<game>\<game>prefs.ini
* My Games\<game>\<game>custom.ini

## **LOOT Preventifier** (LootPreventifier.py, LootPreventifier.zip)

This plugins prevents the user from running "LOOT.exe" or "lootcli.exe" executables through MO2. This is designed to help out mod list authors using Wabbajack and other tools so users are less likely to mess up the load order. The plugin is disabled by default. The user can customize the message displayed when LOOT is detected.

*Note: The intention is for this to block the "sort" button in MO2 as well but this is not functioning with MO quite yet.*

## **RequiemRedirector** (RequiemRedirector.py, LostDragonist-MO2-Plugins.zip)

Disabled by default. This plugin redirects some files to help assist with install Requiem in games other than Skyrim. This is only useful for Requiem 4.0.x. Requiem 5.0.0+ does not need any file shenanigans.

The currently redirected files are:

* %LocalAppData%\Skyrim\plugins.txt -> <active profile>\loadorder.txt
* %LocalAppData%\Skyrim\loadorder.txt -> <active profile>\loadorder.txt

## **Installation**
Extract the archive(s) to your MO2 install directory.

*Note: Updating MO2 with the automated updated/installer will result in these plugins being deleted!  You'll have to reinstall them after updating.*

## Releasing

1. Run src/release.py.
2. Upload zip files.
