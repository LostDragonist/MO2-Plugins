from PyQt5.QtCore import qCritical, qDebug
import os

class GameRedirector(mobase.IPluginFileMapper):
  '''Redirect Skyrim files to Enderal files

  This is mostly useful for tools that are unlikely to receive updates to use
  Enderal specific file locations.  This will add the following redirects:

  %LocalAppData%/Skyrim/plugins.txt   => MO2_Profile/plugins.txt
  %LocalAppData%/Skyrim/loadorder.txt => MO2_Profile/loadorder.txt

  Global INI files:
    My Games/Skyrim/skyrim.ini        => My Games/Enderal/enderal.ini
    My Games/Skyrim/skyrimprefs.ini   => My Games/Enderal/enderalprefs.ini

  Profile-specific INI files\
    My Games/Skyrim/skyrim.ini        => MO2_Profiles/enderal.ini
    My Games/Skyrim/skyrimprefs.ini   => MO2_Profile/enderalprefs.ini
  '''
  def __init__(self):
    super().__init__()
    self.__organizer = None

  def __tr(self, str_):
    return str_

  #==============================================================
  # IPlugin interfaces
  #==============================================================

  def init(self, organizer):
    self.__organizer = organizer
    return True

  def name(self):
    return "Game Redirector"

  def author(self):
    return "LostDragonist"

  def description(self):
    return self.__tr("Redirects game files between different games")

  def version(self):
    return mobase.VersionInfo(3, 0, 0, 0)

  def settings(self):
    return [
      mobase.PluginSetting("enable_enderal", self.__tr("Enable Skyrim->Enderal redirection"), True),
      mobase.PluginSetting("enable_skyrimSE", self.__tr("Enable Skyrim->SkyrimSE redirection"), True),
      mobase.PluginSetting("enable_skyrimVR", self.__tr("Enable SkyrimSE->SkyrimVR redirection"), True),
      ]

  #==============================================================
  # IPluginFileMapper interfaces
  #==============================================================
  def mappings(self):
    '''Gets the redirect mappings.

    Returns:
      A list of Mapping objects.
    '''
    if not self._gameIsSupported():
      return []

    game = self.__organizer.managedGame().gameShortName()
    if (game == "Enderal"):
      result = self._Enderal()
    elif (game == "SkyrimVR"):
      result = self._SkyrimVR()
    elif (game == "SkyrimSE"):
      result = self._SkyrimSE()
    else:
      result = []

    return result

  def _createMapping(self, source, destination, isDirectory=False, createTarget=True):
    obj = mobase.Mapping()
    obj.source = source
    obj.destination = destination
    obj.isDirectory = isDirectory
    obj.createTarget = createTarget
    return obj

  def _redirectGame(self, gameSrcName, gameDstName, iniRedirects):
    qDebug("Setting up {}->{} redirects".format(gameSrcName, gameDstName))
    result = []

    gameSrc = self.__organizer.getGame(gameSrcName)
    gameDst = self.__organizer.getGame(gameDstName)
    profile = self.__organizer.profile()
    profilePath = self.__organizer.profilePath()

    # Redirect AppData files
    for profileFile in ("plugins.txt", "loadorder.txt"):
      result.append(
        self._createMapping(
          source=os.path.join(profilePath, profileFile),
          destination=os.path.expandvars(
            os.path.join("%LOCALAPPDATA%", gameSrc.gameName(), profileFile)
            )
          )
        )

    # Redirect My Games files
    for src, dst in iniRedirects:
      if profile.localSettingsEnabled():
        result.append(
          self._createMapping(
            source=os.path.join(profilePath, dst),
            destination=os.path.join(gameSrc.documentsDirectory().absoluteFilePath(src))
            )
          )
      else:
        result.append(
          self._createMapping(
            source=os.path.join(gameDst.documentsDirectory().absoluteFilePath(dst)),
            destination=os.path.join(gameSrc.documentsDirectory().absoluteFilePath(src))
            )
          )

    return result

  def _gameIsSupported(self):
    game = self.__organizer.managedGame().gameShortName()
    if (game == "Enderal" and self.__organizer.pluginSetting(self.name(), "enable_enderal")):
      return True
    if (game == "SkyrimSE" and self.__organizer.pluginSetting(self.name(), "enable_skyrimSE")):
      return True
    if (game == "SkyrimVR" and self.__organizer.pluginSetting(self.name(), "enable_skyrimVR")):
      return True
    return False

  def _Enderal(self):
    return self._redirectGame("Skyrim", "Enderal", (("skyrim.ini",      "enderal.ini"     ),
                                                    ("skyrimprefs.ini", "enderalprefs.ini")))

  def _SkyrimVR(self):
    return self._redirectGame("SkyrimSE", "SkyrimVR", (("skyrim.ini",       "skyrim.ini"      ),
                                                       ("skyrimprefs.ini",  "skyrimprefs.ini" ),
                                                       ("skyrimcustom.ini", "skyrimcustom.ini")))

  def _SkyrimSE(self):
    return self._redirectGame("Skyrim", "SkyrimSE", (("skyrim.ini",       "skyrim.ini"      ),
                                                     ("skyrimprefs.ini",  "skyrimprefs.ini" )))


def createPlugin():
  return GameRedirector()
