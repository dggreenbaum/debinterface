#! /usr/bin/python

# A class representing the contents of /etc/network/interfaces

import constants
from adapter import NetworkAdapter


class InterfacesReader:

    # Set up the interfaces object.
    def __init__(self):
        # Initialize a place to store created networkAdapter objects.
        self._adapters = []

        # Keep a list of adapters that have the auto or allow-hotplug flags set.
        self._auto_list = []
        self._hotplug_list = []

        # Store the interface context.
        # This is the index of the adapters collection.
        self._context = -1

    # Read /etc/network/interfaces.
    # Return an array of networkAdapter instances.
    def parse_interfaces(self):
        self._read_lines()

        for entry in self._auto_list:
            for adapter in self._adapters:
                if adapter.export()['name'] == entry:
                    adapter.setAuto(True)
        for entry in self._hotplug_list:
            for adapter in self._adapters:
                if adapter.export()['name'] == entry:
                    adapter.setHotplug(True)

        return self._adapters

    def _read_lines(self):
        # Open up the interfaces file. Read only.
        with open(constants.INTERFACES, "r") as interfaces:
            # Loop through the interfaces file.
            for line in interfaces:
                # Identify the clauses by analyzing the first word of each line.
                # Go to the next line if the current line is a comment.
                if line.startswith('#') is True:
                    pass
                else:
                    self._parse_iface()
                    # Ignore blank lines.
                    if line.isspace() is True:
                        pass
                    else:
                        self._parse_details(line)
                    self._read_flags()

    def _parse_iface(self, line):
        # Parse the iface clause
        if line.startswith('iface'):
            sline = line.split()
            # Update the self._context when an iface clause is encountered.
            self._context += 1
            self._adapters.append(NetworkAdapter(sline[1]))
            self._adapters[self._context].setAddressSource(sline[-1])
            if sline[2] == 'inet':
                self._adapters[self._context].setInet(True)

    def _parse_details(self, line):
        # Parse the detail clauses.
        if line[0].isspace() is True:
            sline = line.split()
            if sline[0] == 'address':
                self._adapters[self._context].setAddress(sline[1])
            if sline[0] == 'netmask':
                self._adapters[self._context].setNetmask(sline[1])
            if sline[0] == 'gateway':
                self._adapters[self._context].setGateway(sline[1])
            if sline[0] == 'broadcast':
                self._adapters[self._context].setBroadcast(sline[1])
            if sline[0] == 'network':
                self._adapters[self._context].setNetwork(sline[1])
            if sline[0].startswith('bridge') is True:
                opt = sline[0].split('_')
                sline.pop(0)
                ifs = " ".join(sline)
                self._adapters[self._context].replaceBropt(opt[1], ifs)
            if sline[0] == 'up' or sline[0] == 'down' or sline[0] == 'pre-up' or sline[0] == 'post-down':
                ud = sline.pop(0)
                cmd = ' '.join(sline)
                if ud == 'up':
                    self._adapters[self._context].appendUp(cmd)
                if ud == 'down':
                    self._adapters[self._context].appendDown(cmd)
                if ud == 'pre-up':
                    self._adapters[self._context].appendPreUp(cmd)
                if ud == 'post-down':
                    self._adapters[self._context].appendPostDown(cmd)

    def _read_flags(self):
        # Identify which adapters are flagged with auto and allow-hotplug.
        if line.startswith('auto'):
            sline = line.split()
            for word in sline:
                if word == 'auto':
                    pass
                else:
                    self._auto_list.append(word)
        if line.startswith('allow-hotplug'):
            sline = line.split()
            for word in sline:
                if word == 'allow-hotplug':
                    pass
                else:
                    self._hotplug_list.append(word)
                    # Set the auto and allow-hotplug options for each adapter.
