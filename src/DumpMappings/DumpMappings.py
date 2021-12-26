import sys
import ctypes

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox


class MappingDumper(mobase.IPlugin):
    def __init__(self):
        super().__init__()
        self._organizer = None
        self._parent = None

    def enabledByDefault(self):
        return False

    def __tr(self, str_):
        return QCoreApplication.translate(self.name(), str_)

    def init(self, organizer):
        """
        Initializes the plugin and provides the main reference to the application
        """
        self._organizer = organizer
        if not self._organizer.onFinishedRun(
            lambda appName, result: self._dumpMappings()
        ):
            print("Failed to register onFinishedRun callback!", file=sys.stderr)
            return False
        return True

    def name(self):
        """
        Name of the plugin for mostly internal uses.
        Will be displayed in the plugin settings tab.
        Do not translate.
        """
        return "MappingDumper"

    def author(self):
        """
        Author as seen in the plugin settings tab.
        Do not translate.
        """
        return "LostDragonist"

    def description(self):
        """
        Description as seen in the plugin settings tab.
        May be translated.
        """
        return self.__tr("Dumps the USVFS mappings when running an executable")

    def version(self):
        """
        Version as seen in the plugin settings tab.
        """
        return mobase.VersionInfo(1, 0, 0, 0)

    def settings(self):
        """
        List of user-accessible settings for the plugin.
        May return empty list.
        """
        return []

    def _dumpMappings(self):
        # usvfs = ctypes.CDLL(r"C:\Modding\Mod Organizer\2.4.1\usvfs_x64.dll")
        usvfs = ctypes.CDLL("usvfs_x64.dll")

        # DLLEXPORT BOOL WINAPI CreateVFSDump(LPSTR buffer, size_t *size);
        # Note: CreateVFSDump returns a failure when required_size is not big enough
        #       even though the output buffer is NULL???
        required_size = ctypes.c_size_t()
        usvfs.CreateVFSDump(0, ctypes.byref(required_size))
        buffer = ctypes.create_string_buffer(required_size.value)

        if not usvfs.CreateVFSDump(buffer, ctypes.byref(required_size)):
            print("failed to get USVFS dump", file=sys.stderr)
            return True

        with open(
            os.path.join(self._organizer.overwritePath(), "usvfs_dump.log"), "w"
        ) as f:
            f.write(buffer.value.decode("cp1252"))

        return True


def createPlugin():
    return MappingDumper()
