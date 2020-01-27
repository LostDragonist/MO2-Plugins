from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

class PluginToolTemplate(mobase.IPluginTool):
    def __init__(self):
        super().__init__()
        self._organizer = None
        self._parent = None

    def __tr(self, str_):
        return QCoreApplication.translate(self.name(), str_)

    def init(self, organizer):
        '''
        Initializes the plugin and provides the main reference to the application
        '''
        self._organizer = organizer
        return True

    def name(self):
        '''
        Name of the plugin for mostly internal uses.  
        Will be displayed in the plugin settings tab.
        Do not translate.
        '''
        return "PluginToolTemplate"

    def author(self):
        '''
        Author as seen in the plugin settings tab.  
        Do not translate.
        '''
        return "Author"

    def description(self):
        '''
        Description as seen in the plugin settings tab.
        May be translated.
        '''
        return self.__tr("Description")

    def version(self):
        '''
        Version as seen in the plugin settings tab.
        '''
        return mobase.VersionInfo(0, 0, 0, 0)

    def isActive(self):
        '''
        Return true if plugin should be active for a given game and configuration, 
        and false otherwise.  Inactive plugins will not be displayed in menus and their
        notifications will be ignored.  They will still appear in the plugin settings
        tab.
        '''
        return self._organizer.pluginSetting(self.name(), "enabled")

    def settings(self):
        '''
        List of user-accessible settings for the plugin.
        May return empty list.
        '''
        return [                # name      description                      default
            mobase.PluginSetting("enabled", self.__tr("Enables the plugin"), True),
            ]

    def displayName(self):
        '''
        The clickable action in the tools menu.
        May be nested into a sub-menu with a slash.
        '''
        return self.__tr("Templates/PluginToolTemplate")

    def tooltip(self):
        '''
        The tooltip displayed when hovering over the action in the tools menu.
        '''
        return self.__tr("This is just an example")

    def icon(self):
        '''
        Icon displayed to the left of the action in the tools menu.
        '''
        return QIcon()

    def setParentWidget(self, widget):
        '''
        Sets the parent widget to be used for displaying dialogs.
        Called before display() is called.
        '''
        self._parent = widget

    def display(self):
        '''
        The action has been clicked!  Do the thing!
        '''
        pass

    
def createPlugin():
    return PluginToolTemplate()