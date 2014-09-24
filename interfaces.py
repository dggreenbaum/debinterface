# A class representing the contents of /etc/network/interfaces
from interfacesWriter import InterfacesWriter
from interfacesReader import InterfacesReader
from adapter import NetworkAdapter
import tools


class Interfaces:
    def __init__(self, read_interface=True):
        ''' By default read interface file on init '''

        if read_interface:
            self._adapters = self.parseInterfaces()
        if not self._adapters:
            self._adapters = []

    @property
    def adapters(self):
        return self._adapters

    def parseInterfaces(self):
        ''' Read /etc/network/interfaces.
            Return an array of networkAdapter instances.
        '''
        return InterfacesReader().parse_interfaces()

    def addAdapter(self, options, index=None):
        ''' Insert a networkAdapter before the given index or at the end of the list. '''
        if index is None:
            self._adapters.insert(index, NetworkAdapter(options))
        else:
            self._adapters.append(NetworkAdapter(options))

    def removeAdapter(self, index):
        ''' Remove the adapter at the given index. '''
        self._adapters.pop(index)

    def writeInterfaces(self):
        return InterfacesWriter(self._adapters).write_interfaces()

    def controlNetworkService(self, action):
        ''' return True/False, command output '''

        if action not in ["start", "stop", "restart"]:
            return False, "Invalid action"
        return tools.safe_subprocess(["/etc/init.d/networking", action])
