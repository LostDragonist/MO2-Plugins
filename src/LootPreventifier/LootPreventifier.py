from PyQt5.QtCore import QCoreApplication, qCritical, QDir, qDebug
from PyQt5.QtWidgets import QMessageBox

class LootPreventifier(mobase.IPlugin):

    def __init__(self):
        super().__init__()
        self._organizer = None
        self._parent = None

    def __tr(self, str_):
        return QCoreApplication.translate("LootPreventifier", str_)

    # IPlugin
    def init(self, organizer):
        self._organizer = organizer
        if (not self._organizer.onAboutToRun(lambda appName: self._preventLoot(appName))):
            qCritical("Failed to register onAboutToRun callback!")
            return False
        return True

    def name(self):
        return "LOOT Preventifier"

    def author(self):
        return "LostDragonist"

    def description(self):
        return self.__tr("Prevents the user from running LOOT")

    def version(self):
        return mobase.VersionInfo(0, 0, 2, 0)

    def settings(self):
        return [
            mobase.PluginSetting("dialog", self.__tr("String displayed when LOOT is ran"),
                                 "This load order was created by hand and is carefully curated. "
                                 "Running LOOT is disabled.")
            ]

    def _preventLoot(self, appName):
        if (appName.lower().endswith("loot.exe") or appName.lower().endswith("lootcli.exe")):
            dialog = self._organizer.pluginSetting(self.name(), "dialog")
            if dialog != '':
                QMessageBox.information(self._parent, self.name(), dialog)
            return False
        return True

def createPlugin():
    return LootPreventifier()