from PyQt5.QtCore import qCritical, qDebug
import os

class RequiemRedirector(mobase.IPluginFileMapper):
    '''Redirect Skyrim files to assist with Requiem installs'''
    def __init__(self):
        super().__init__()
        self._organizer = None

    def __tr(self, str_):
        return str_

    #==============================================================
    # IPlugin interfaces
    #==============================================================

    def init(self, organizer):
        self.__organizer = organizer
        return True

    def name(self):
        return "Requiem Installer"

    def author(self):
        return "LostDragonist"

    def description(self):
        return self.__tr("Redirect Skyrim files to assist with Requiem installs")

    def version(self):
        return mobase.VersionInfo(1, 0, 0, 0)

    def settings(self):
        return []

    def enabledByDefault(self):
        return False

    #==============================================================
    # IPluginFileMapper interfaces
    #==============================================================
    def mappings(self):
        '''Gets the redirect mappings.

        Returns:
        A list of Mapping objects.
        '''
        return self._redirectPlugins()

    def _createMapping(self, source, destination, isDirectory=False, createTarget=True):
        obj = mobase.Mapping()
        obj.source = source
        obj.destination = destination
        obj.isDirectory = isDirectory
        obj.createTarget = createTarget
        return obj

    def _redirectPlugins(self):
        result = []

        gameSrc = self.__organizer.getGame("Skyrim")
        gameDst = self.__organizer.managedGame()
        profile = self.__organizer.profile()
        profilePath = self.__organizer.profilePath()

        # Don't redirect Skyrim to Skyrim
        if (gameSrc == gameDst):
            return result

        # Redirect AppData files
        for profileFile in ("plugins.txt", "loadorder.txt"):
            result.append(
                self._createMapping(
                    source=os.path.join(profilePath, "loadorder.txt"),
                    destination=os.path.expandvars(
                        os.path.join("%LOCALAPPDATA%", "Skyrim", profileFile)
                    )
                )
            )

        return result

def createPlugin():
  return RequiemRedirector()
