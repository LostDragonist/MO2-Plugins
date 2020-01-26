## **Description**

This is a collection of [Mod Organizer 2 (MO2)](https://www.nexusmods.com/skyrimspecialedition/mods/6194)﻿ plugins created by me, LostDragonist!  These are plugins that, for some reason or another, aren't included in the main release of MO2.  

See mirrors section for Github link.

## **Included Plugins**

## **Fix Game Registry Key** (FixGameRegKey.py)

When running an application in MO2, this will check to make sure the registry key is correct according to the game being managed by MO2.  This is useful when you have moved the game, when you've validated a game with Steam, when the game has updated, or if you have multiple installations of the game with different MO2 instances pointing to different installs.

Whenever the registry needs to be changed, a User Account Control (UAC) prompt may show up from the Registry Console Tool.  You need to accept this for the change to occur!

For what it's worth, this functionality requires Powershell to be installed.  Any modern Windows PC should have Powershell.

## **Game Redirector** (GameRedirector.py)

This plugin maps certain game files for some games to the game files used by other games.  This is useful when mods/installers/tools are *technically* compatible with multiple games but may not be updated or might have some issues.  For example, running the Requiem patcher for Skyrim SE has some problems if you already have Skyrim installed and this might fix it!

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

## **Installation**
Extract the archive to your MO2 install directory.

## *Note: Updating MO2 with the automated updated/installer will result in these plugins being deleted!  You'll have to reinstall them after updating.*

## Releasing

1. Run src/release.py.  
2. Upload release.zip.
