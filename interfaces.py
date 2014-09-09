#! /usr/bin/python

# A class representing the contents of /etc/network/interfaces

from interfacesWriter import InterfacesWriter
from interfacesReader import InterfacesReader
from adapter import NetworkAdapter


class Interfaces:

    # Set up the interfaces object.
    def __init__(self):
        self.adapters = self.parseInterfaces()

    # Read /etc/network/interfaces.
    # Return an array of networkAdapter instances.
    def parseInterfaces(self):
        reader = InterfacesReader()
        return reader.parse_interfaces()

    # Insert a networkAdapter before the given index or at the end of the list.
    def addAdapter(self, options, index=None):
        if index is None:
            self.adapters.insert(index, NetworkAdapter(options))
        else:
            self.adapters.append(NetworkAdapter(options))

    # Remove the adapter at the given index.
    def removeAdapter(self, index):
        self.adapters.pop(index)

    def writeInterfaces(self):
        writer = InterfacesWriter(self.adapters)
        writer.write_interfaces()
