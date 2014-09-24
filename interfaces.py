# A class representing the contents of /etc/network/interfaces
from interfacesWriter import InterfacesWriter
from interfacesReader import InterfacesReader
from adapter import NetworkAdapter
import tools
import defaults


class Interfaces:
    def __init__(self, update_adapters=True, interfaces_path=None, backup_path=None):
        ''' By default read interface file on init '''

        self._set_paths(interfaces_path, backup_path)

        if update_adapters is True:
            self.updateAdapters()
        else:
            self._adapters = []

    @property
    def adapters(self):
        return self._adapters

    @property
    def interfaces_path(self):
        return self._interfaces_path

    @property
    def backup_path(self):
        return self._backup_path

    def updateAdapters(self):
        ''' (re)read interfaces file and save adapters '''
        self._adapters = InterfacesReader(self._interfaces_path).parse_interfaces()
        if not self._adapters:
            self._adapters = []

    def writeInterfaces(self):
        ''' write adapters to interfaces file '''
        return InterfacesWriter(
            self._adapters,
            self._interfaces_path,
            self._backup_path
        ).write_interfaces()

    def addAdapter(self, options, index=None):
        ''' Insert a networkAdapter before the given index or at the end of the list. '''
        if index is None:
            self._adapters.insert(index, NetworkAdapter(options))
        else:
            self._adapters.append(NetworkAdapter(options))

    def removeAdapter(self, index):
        ''' Remove the adapter at the given index. '''
        self._adapters.pop(index)

    def controlNetworkService(self, action):
        ''' return True/False, command output '''

        if action not in ["start", "stop", "restart"]:
            return False, "Invalid action"
        return tools.safe_subprocess(["/etc/init.d/networking", action])

    def _set_paths(self, interfaces_path, backup_path):
        ''' either use user input or defaults '''

        if interfaces_path is not None:
            self._interfaces_path = interfaces_path
        else:
            self._interfaces_path = defaults.INTERFACES_PATH

        if backup_path is not None:
            self._backup_path = backup_path
        else:
            self._backup_path = defaults.BACKUP_PATH
