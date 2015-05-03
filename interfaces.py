# A class representing the contents of /etc/network/interfaces
from interfacesWriter import InterfacesWriter
from interfacesReader import InterfacesReader
from adapter import NetworkAdapter
import toolutils
#import defaults


class Interfaces:
    _interfaces_path = '/etc/network/interfaces'

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

    def updateAdaptersWithString(self, data):
        self._adapters = InterfacesReader(None).parse_interfaces_from_string(data)
        if not self._adapters:
            self._adapters = []

    def writeInterfaces(self):
        ''' write adapters to interfaces file '''
        self._writer_factory().write_interfaces()

    def writeInterfacesAsString(self):
        return self._writer_factory().write_interfaces_as_string()

    def _writer_factory(self):
        ''' Create a writer object '''
        return InterfacesWriter(
            self._adapters,
            self._interfaces_path,
            self._backup_path
        )

    def getAdapter(self, name):
        ''' Find adapter by interface name '''
        return next((x for x in self._adapters if x._ifAttributes['name'] == name), None)

    def addAdapter(self, options, index=None):
        '''
            Insert a networkAdapter before the given index or at the end of the list.
            options should be a string (name) or a dict
        '''
        adapter = NetworkAdapter(options)
        adapter.validateAll()

        if index:
            self._adapters.insert(index, adapter)
        else:
            self._adapters.append(adapter)
        return adapter

    def removeAdapter(self, index):
        ''' Remove the adapter at the given index. '''
        self._adapters.pop(index)

    def removeAdapterByName(self, name):
        ''' Remove the adapter with the given name. '''
        self._adapters = [x for x in self._adapters if x._ifAttributes['name'] != name]

    def upAdapter(self, if_name):
        ''' return True/False, command output. Use ifconfig. '''

        return toolutils.safe_subprocess(["ifconfig", if_name, 'up'])

    def downAdapter(self, if_name):
        ''' return True/False, command output. Use ifdown. '''

        return toolutils.safe_subprocess(["ifconfig", if_name, 'down'])

    def _set_paths(self, interfaces_path, backup_path):
        ''' either use user input or defaults '''

        if interfaces_path is not None:
            self._interfaces_path = interfaces_path

        if backup_path:
            self._backup_path = backup_path
        else:
            self._backup_path = self._interfaces_path + ".bak"
