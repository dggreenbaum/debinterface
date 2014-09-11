#! /usr/bin/python

# A class representing the contents of /etc/network/interfaces
from interfacesWriter import InterfacesWriter
from interfacesReader import InterfacesReader
from adapter import NetworkAdapter
import tools


class Interfaces:
    def __init__(self):
        self.adapters = self.parseInterfaces()

    def parseInterfaces(self):
        ''' Read /etc/network/interfaces.
            Return an array of networkAdapter instances.
        '''
        return InterfacesReader().parse_interfaces()

    def addAdapter(self, options, index=None):
        ''' Insert a networkAdapter before the given index or at the end of the list. '''
        if index is None:
            self.adapters.insert(index, NetworkAdapter(options))
        else:
            self.adapters.append(NetworkAdapter(options))

    def removeAdapter(self, index):
        ''' Remove the adapter at the given index. '''
        self.adapters.pop(index)

    def writeInterfaces(self):
        return InterfacesWriter(self.adapters).write_interfaces()

    def stopNetworkService(self):
        ''' return True/False, command output '''
        return tools.safe_subprocess(["/etc/init.d/networking", "stop"])

    def startNetworkService(self):
        ''' return True/False, command output '''
        return tools.safe_subprocess(["/etc/init.d/networking", "start"])

    def restartNetworkService(self):
        ''' return True/False, command output '''
        return tools.safe_subprocess(["/etc/init.d/networking", "restart"])
