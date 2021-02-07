from PyQt5.QtCore import QCoreApplication, qCritical, QDir, qDebug
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

import os
import shutil
import subprocess
import winreg

class FixGameRegKey(mobase.IPluginTool):

    GAME_REGISTRY_KEYS = {
        "Enderal":    (winreg.HKEY_LOCAL_MACHINE, "Software\\SureAI\\Enderal",                            "Install_Path"),
        "Fallout3":   (winreg.HKEY_LOCAL_MACHINE, "Software\\Bethesda Softworks\\Fallout3",               "Installed Path"),
        "Fallout4":   (winreg.HKEY_LOCAL_MACHINE, "Software\\Bethesda Softworks\\Fallout4",               "Installed Path"),
        "Fallout4VR": (winreg.HKEY_LOCAL_MACHINE, "Software\\Bethesda Softworks\\Fallout 4 VR",           "Installed Path"),
        "FalloutNV":  (winreg.HKEY_LOCAL_MACHINE, "Software\\Bethesda Softworks\\FalloutNV",              "Installed Path"),
        "Morrowind":  (winreg.HKEY_LOCAL_MACHINE, "Software\\Bethesda Softworks\\Morrowind",              "Installed Path"),
        "Oblivion":   (winreg.HKEY_LOCAL_MACHINE, "Software\\Bethesda Softworks\\Oblivion",               "Installed Path"),
        "Skyrim":     (winreg.HKEY_LOCAL_MACHINE, "Software\\Bethesda Softworks\\Skyrim",                 "Installed Path"),
        "SkyrimSE":   (winreg.HKEY_LOCAL_MACHINE, "Software\\Bethesda Softworks\\Skyrim Special Edition", "Installed Path"),
        "SkyrimVR":   (winreg.HKEY_LOCAL_MACHINE, "Software\\Bethesda Softworks\\Skyrim VR",              "Installed Path"),
        "TTW":        (winreg.HKEY_LOCAL_MACHINE, "Software\\Bethesda Softworks\\FalloutNV",              "Installed Path"),
        }

    def __init__(self):
        super().__init__()
        self._organizer = None
        self._parent = None
        self._powershellFound = shutil.which('powershell') is not None

    def __tr(self, str_):
        return QCoreApplication.translate("FixGameRegKey", str_)

    # IPlugin
    def init(self, organizer):
        self._organizer = organizer
        if (not self._organizer.onAboutToRun(lambda appName: self._checkInstallPath())):
            qCritical("Failed to register onAboutToRun callback!")
            return False
        return True

    def name(self):
        return "Fix Game Registry Key"

    def author(self):
        return "LostDragonist"

    def description(self):
        return self.__tr("Checks the game's installation path registry key and fixes as needed")

    def version(self):
        return mobase.VersionInfo(1, 0, 0, 0)



    def settings(self):
        return [
            mobase.PluginSetting("silent", self.__tr("Fix the registry automatically"), False),
            ]

    # IPluginTool
    def displayName(self):
        return self.__tr("Check Game Registry Key")

    def tooltip(self):
        return self.description()

    def icon(self):
        return QIcon()

    def setParentWidget(self, widget):
        self._parent = widget

    def display(self):
        if self._isActive():
           self._checkInstallPath()

    def _isActive(self):
        if self._getGameRegistryInfo() is None:
            active = False
        elif not self._powershellFound:
            active = False
        else:
            active = True
        return active

    def _checkInstallPath(self):
        if not self._isActive():
            return True

        gameDirectory = self._organizer.managedGame().gameDirectory().canonicalPath()
        installPath = self._readInstallPath()
        if (gameDirectory != installPath):
            if (gameDirectory == ''):
                gameDirectory = self.__tr('<invalid path>')
            if (installPath == ''):
                installPath = self.__tr('<invalid path>')
            answer = QMessageBox.question(self._parent,
                                          self.__tr("Registry key does not match"),
                                          self.__tr("The game's installation path in the registry does not match the managed game path in MO.\n\n"
                                          "Registry Game Path:\n\t{}\n"
                                          "Managed Game Path:\n\t{}\n\n"
                                          "Change the path in the registry to match the managed game path?").format(installPath, gameDirectory),
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                          QMessageBox.Yes)
            if (answer == QMessageBox.Yes):
                self._writeInstallPath()
            elif (answer == QMessageBox.Cancel):
                return False
        return True

    def _readInstallPath(self):
        key, subKey, valueName = self._getGameRegistryInfo()
        try:
            with winreg.OpenKey(key, subKey, 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY) as hKey:
                try:
                    installPath, _ = winreg.QueryValueEx(hKey, valueName)
                    installPath = QDir(installPath).canonicalPath()
                except FileNotFoundError:
                    installPath = ''
        except FileNotFoundError:
            installPath = ''
        return installPath

    def _writeInstallPath(self):
        # Figure out what MO is configured to
        gameDirectory = self._organizer.managedGame().gameDirectory().canonicalPath()

        # Get the registry info and check for possible problems
        key, subKey, valueName = self._getGameRegistryInfo()
        if (key != winreg.HKEY_LOCAL_MACHINE):
            qCritical("Only HKLM is supported!")
            return

        # Use powershell to write to the registry as admin
        args = '\'add "{}\\{}" /v "{}" /d "{}" /f /reg:32\''.format("HKLM", subKey, valueName, gameDirectory.replace("'", "''"))
        cmd = ['powershell', 'Start-Process', '-Verb', 'runAs', 'reg', '-ArgumentList', args]
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            qDebug("Running the command \"{}\"".format(" ".join(cmd)))
            subprocess.check_call(cmd, startupinfo=si)
        except subprocess.CalledProcessError as e:
            qCritical("Powershell non-zero exit status: {}, {}".format(e.returncode, e.output))

    def _getGameRegistryInfo(self):
        gameName = self._organizer.managedGame().gameShortName()
        if gameName in self.GAME_REGISTRY_KEYS:
            return self.GAME_REGISTRY_KEYS[gameName]
        else:
            return None

def createPlugin():
    return FixGameRegKey()