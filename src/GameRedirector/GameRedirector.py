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
    super(GameRedirector, self).__init__()
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
    return mobase.VersionInfo(2, 0, 0, 0)

  def isActive(self):
    return ( self.__organizer.pluginSetting(self.name(), "enabled") and 
             self.__organizer.managedGame().gameShortName() in self._supportedGames() )

  def settings(self):
    return [
      mobase.PluginSetting("enabled", self.__tr("Enable plugin"), True)
      ]

  def _supportedGames(self):
    return ["Enderal", "SkyrimVR", "SkyrimSE"]

  #==============================================================
  # IPluginFileMapper interfaces
  #==============================================================
  def mappings(self):
    '''Gets the redirect mappings.

    Returns:
      A list of Mapping objects.
    '''
    if not self.__organizer.pluginSetting(self.name(), "enabled"):
      return []
    
    game = self.__organizer.managedGame.gameShortName()
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
    
  def _Enderal(self):
    result = []

    gameSkyrim = self.__organizer.getGame("Skyrim")
    gameEnderal = self.__organizer.getGame("Enderal")
    profile = self.__organizer.profile()
    profilePath = self.__organizer.profilePath()

    # Redirect AppData files
    for profileFile in ("plugins.txt", "loadorder.txt"):
      result.append(
        self._createMapping(
          source=os.path.join(profilePath, profileFile),
          destination=os.path.expandvars(
            os.path.join("%LOCALAPPDATA%", gameSkyrim.gameShortName(), profileFile)
            )
          )
        )

    #Redirect My Games files
    for src, dst in (("skyrim.ini", "enderal.ini"),
                     ("skyrimprefs.ini", "enderalprefs.ini")):
      if profile.localSettingsEnabled():
        result.append(
          self._createMapping(
            source=os.path.join(profilePath, dst),
            destination=os.path.join(gameSkyrim.documentsDirectory().absoluteFilePath(src))
            )
          )
      else:
        result.append(
          self._createMapping(
            source=os.path.join(gameEnderal.documentsDirectory().absoluteFilePath(dst)),
            destination=os.path.join(gameSkyrim.documentsDirectory().absoluteFilePath(src))
            )
          )

    return result

  def _SkyrimVR(self):
    result = []

    gameSkyrimVR = self.__organizer.getGame("SkyrimVR")
    gameSkyrimSE = self.__organizer.getGame("SkyrimSE")
    profile = self.__organizer.profile()
    profilePath = self.__organizer.profilePath()

    # Redirect AppData files
    for profileFile in ("plugins.txt", "loadorder.txt"):
      result.append(
        self._createMapping(
          source=os.path.join(profilePath, profileFile),
          destination=os.path.expandvars(
            os.path.join("%LOCALAPPDATA%", gameSkyrimVR.gameShortName(), profileFile)
            )
          )
        )

    #Redirect My Games files
    for src, dst in (("skyrim.ini", "skyrim.ini"),
                     ("skyrimprefs.ini", "skyrimprefs.ini"),
                     ("skyrimcustom.ini", "skyrimcustom.ini")):
      if profile.localSettingsEnabled():
        result.append(
          self._createMapping(
            source=os.path.join(profilePath, dst),
            destination=os.path.join(gameSkyrimVR.documentsDirectory().absoluteFilePath(src))
            )
          )
      else:
        result.append(
          self._createMapping(
            source=os.path.join(gameSkyrimSE.documentsDirectory().absoluteFilePath(dst)),
            destination=os.path.join(gameSkyrimVR.documentsDirectory().absoluteFilePath(src))
            )
          )

    return result

  def _SkyrimSE(self):
    result = []

    gameSkyrimSE = self.__organizer.getGame("SkyrimSE")
    gameSkyrim = self.__organizer.getGame("Skyrim")
    profile = self.__organizer.profile()
    profilePath = self.__organizer.profilePath()

    # Redirect AppData files
    for profileFile in ("plugins.txt", "loadorder.txt"):
      result.append(
        self._createMapping(
          source=os.path.join(profilePath, profileFile),
          destination=os.path.expandvars(
            os.path.join("%LOCALAPPDATA%", gameSkyrimSE.gameShortName(), profileFile)
            )
          )
        )

    #Redirect My Games files
    for src, dst in (("skyrim.ini", "skyrim.ini"),
                     ("skyrimprefs.ini", "skyrimprefs.ini"),
                     ("skyrimcustom.ini", "skyrimcustom.ini")):
      if profile.localSettingsEnabled():
        result.append(
          self._createMapping(
            source=os.path.join(profilePath, dst),
            destination=os.path.join(gameSkyrimSE.documentsDirectory().absoluteFilePath(src))
            )
          )
      else:
        result.append(
          self._createMapping(
            source=os.path.join(gameSkyrim.documentsDirectory().absoluteFilePath(dst)),
            destination=os.path.join(gameSkyrimSE.documentsDirectory().absoluteFilePath(src))
            )
          )

    return result



def createPlugin():
  return GameRedirector()
