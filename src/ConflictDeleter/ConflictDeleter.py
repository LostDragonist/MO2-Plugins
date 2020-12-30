from PyQt5.QtCore import QCoreApplication, qCritical, QDir, qDebug
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

import os
import pathlib
import shutil
import subprocess
import time
import winreg

class ConflictDeleter(mobase.IPluginTool):

    def __init__(self):
        super().__init__()
        self._organizer = None
        self._parent = None

    def __tr(self, str_):
        return QCoreApplication.translate("ConflictDeleter", str_)

    # IPlugin
    def init(self, organizer):
        self._organizer = organizer
        return True

    def name(self):
        return "Conflict Deleter"

    def author(self):
        return "LostDragonist"

    def description(self):
        return self.__tr("Removes files that are overwritten by other mods")

    def version(self):
        return mobase.VersionInfo(0, 2, 0, 0)

    def isActive(self):
        if not self._organizer.pluginSetting(self.name(), "enabled"):
            active = False
        else:
            active = True
        return active

    def settings(self):
        return [
            mobase.PluginSetting("enabled", self.__tr("Enables the plugin"), True),
            ]

    # IPluginTool
    def displayName(self):
        return self.__tr("Conflict Deleter")

    def tooltip(self):
        return self.description()

    def icon(self):
        return QIcon()

    def setParentWidget(self, widget):
        self._parent = widget

    def display(self):
        if self.isActive():
           self._deleteConflicts()

    def _deleteConflicts(self):
        if not self.isActive():
            return True

        # Figure out a name for the mod that contains the "deleted" files
        backup_mod_name = time.strftime("ConflictDeleter_Backup_%Y_%m_%d_%H_%M_%S")

        # Check to see if the mod exists first
        if self._organizer.getMod(backup_mod_name) != None:
            QMessageBox.critical(self.__parent,
                                 self.__tr("Mod already exists!"),
                                 self.__tr("Mod \"{}\" already exists. Please run again!").format(backup_mod_name))

        # Ask the user
        answer = QMessageBox.question(self._parent,
                                      self.__tr("Delete Conflicts?"),
                                      self.__tr("Do you want to delete all files that are overwritten by higher priority mods?\n\n"
                                                "Backup folder: {}").format(backup_mod_name),
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        if (answer != QMessageBox.Yes):
            return False

        # Find files to delete
        files_to_delete = {} # key = mod, value = file

        mods_directory = self._organizer.modsPath()

        dirs_to_search = ['']
        self._listDirsRecursive(dirs_to_search)

        for dir_ in dirs_to_search:
            for file_ in self._organizer.findFiles(path=dir_, filter=lambda x: True):
                # This is a messed up way to discard the mods directory and mod name from the path
                try:
                    file_ = os.path.join(*pathlib.Path(file_).relative_to(mods_directory).parts[1:])
                except ValueError:
                    # Skip files not in the mods directory
                    continue

                origins = self._organizer.getFileOrigins(file_)
                if len(origins) > 1:
                    for origin in origins[1:]:
                        if origin not in files_to_delete:
                            files_to_delete[origin] = [file_]
                        else:
                            files_to_delete[origin].append(file_)

        # Create the backup mod
        backup_mod = self._organizer.createMod(mobase.GuessedString(value=backup_mod_name,
                                                                    quality=mobase.GuessQuality.PRESET))
        backup_mod_path = backup_mod.absolutePath()

        # Move files around
        for mod_name in files_to_delete:
            mod = self._organizer.getMod(mod_name)
            if mod is None:
                qDebug("Unable to get mod: {}".format(mod_name.encode('utf-8')))
                continue
            mod_path = mod.absolutePath()
            if not mod_path.startswith(mods_directory):
                # Probably DLC or unmanaged mod
                continue
            for file_ in files_to_delete[mod_name]:
                src_path = os.path.join(mod_path, file_)
                if os.path.exists(src_path):
                    dst_path = os.path.join(backup_mod_path, mod_name, file_)
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.move(src_path, dst_path)

            # Delete empty folders in mod
            self._removeEmptyFoldersRecursive(mod_path, mod_path)

            # Refresh the mod
            self._organizer.modDataChanged(mod)

        # Refresh backup mod
        self._organizer.modDataChanged(backup_mod)

    def _listDirsRecursive(self, dirs_list, prefix=""):
        dirs = self._organizer.listDirectories(prefix)
        for dir_ in dirs:
            dir_ = os.path.join(prefix, dir_)
            dirs_list.append(dir_)
            self._listDirsRecursive(dirs_list, dir_)

    def _removeEmptyFoldersRecursive(self, path, root):
        # Enumerate to find all sub-directories and recurse
        files = os.listdir(path)
        for file_ in files:
            child_path = os.path.join(path, file_)
            if os.path.isdir(child_path):
                self._removeEmptyFoldersRecursive(child_path, root)

        # Re-enumerate to find files
        files = os.listdir(path)
        if len(files) == 0 and path != root:
            os.rmdir(path)

def createPlugin():
    return ConflictDeleter()
