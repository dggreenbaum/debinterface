#! /usr/bin/python

# A class representing the contents of /etc/network/interfaces

from . import constants

from .adapter import *

class interfaces:
    # Read /etc/network/interfaces.
    # Return an array of networkAdapter instances.
    def parseInterfaces(self):
        from .adapter import networkAdapter

        # Open up the interfaces file. Read only.
        interfaces = open(constants.INTERFACES, "r")

        # Initialize a place to store created networkAdapter objects.
        adapters = []

        # Keep a list of adapters that have the auto or allow-hotplug flags set.
        auto_list = []
        hotplug_list = []

        # Store the interface context.
        # This is the index of the adapters collection.
        context = -1

        # Loop through the interfaces file.
        for line in interfaces:
            # Identify the clauses by analyzing the first word of each line.
            # Go to the next line if the current line is a comment.
            if line.startswith('#') == True:
                pass
            else:
                # Parse the iface clause
                if line.startswith('iface'):
                    sline = line.split()
                    # Update the context when an iface clause is encountered.
                    context += 1
                    adapters.append(networkAdapter(sline[1]))
                    adapters[context].setAddressSource(sline[-1])
                    if sline[2] == 'inet':
                        adapters[context].setInet(True)
                        # Ignore blank lines.
                if line.isspace() == True:
                    pass
                else:
                    # Parse the detail clauses.
                    if line[0].isspace() == True:
                        sline = line.split()
                        if sline[0] == 'address':
                            adapters[context].setAddress(sline[1])
                        if sline[0] == 'netmask':
                            adapters[context].setNetmask(sline[1])
                        if sline[0] == 'gateway':
                            adapters[context].setGateway(sline[1])
                        if sline[0] == 'broadcast':
                            adapters[context].setBroadcast(sline[1])
                        if sline[0] == 'network':
                            adapters[context].setNetwork(sline[1])
                        if sline[0].startswith('bridge') == True:
                            opt = sline[0].split('_')
                            sline.pop(0)
                            ifs = " ".join(sline)
                            adapters[context].replaceBropt(opt[1], ifs)
                        if sline[0] == 'up' or sline[0] == 'down' or sline[0] == 'pre-up' or sline[0] == 'post-down':
                            ud = sline.pop(0)
                            cmd = ' '.join(sline)
                            if ud == 'up':
                                adapters[context].appendUp(cmd)
                            if ud == 'down':
                                adapters[context].appendDown(cmd)
                            if ud == 'pre-up':
                                adapters[context].appendPreUp(cmd)
                            if ud == 'post-down':
                                adapters[context].appendPostDown(cmd)

                # Identify which adapters are flagged with auto and allow-hotplug.
                if line.startswith('auto'):
                    sline = line.split()
                    for word in sline:
                        if word == 'auto':
                            pass
                        else:
                            auto_list.append(word)
                if line.startswith('allow-hotplug'):
                    sline = line.split()
                    for word in sline:
                        if word == 'allow-hotplug':
                            pass
                        else:
                            hotplug_list.append(word)
                            # Set the auto and allow-hotplug options for each adapter.
        for entry in auto_list:
            for adapter in adapters:
                if adapter.export()['name'] == entry:
                    adapter.setAuto(True)
        for entry in hotplug_list:
            for adapter in adapters:
                if adapter.export()['name'] == entry:
                    adapter.setHotplug(True)

        return adapters

    # Insert a networkAdapter before the given index or at the end of the list.
    def addAdapter(self, options, index=None):

        if index != None:
            self.adapters.insert(index, networkAdapter(options))
        else:
            self.adapters.append(networkAdapter(options))

    # Remove the adapter at the given index.
    def removeAdapter(self, index):
        self.adapters.pop(index)

    def writeInterfaces(self):

        # Back up the old interfaces file.
        import subprocess

        subprocess.call(["mv", constants.INTERFACES, constants.BACKUP])

        # Prepare to write the new interfaces file.
        interfaces = open(constants.INTERFACES, "a")

        # Loop through the provided networkAdaprers and write the new file.
        for adapter in self.adapters:
            # Get dict of details about the adapter.
            ifAttributes = adapter.export()

            # Write auto and allow-hotplug clauses if applicable.
            try:
                if adapter.ifAttributes['auto'] == True:
                    d = dict(name=ifAttributes['name'])
                    interfaces.write(self.AUTO.substitute(d))
            except KeyError:
                pass

            try:
                if ifAttributes['hotplug'] == True:
                    d = dict(name=adapter.ifAttributes['name'])
                    interfaces.write(self.HOTPLUG.substitute(d))
            except KeyError:
                pass

            # Construct and write the iface declaration.
            # The inet clause needs a little more processing.
            if ifAttributes['inet'] == True:
                inet_val = 'inet'
            else:
                inet_val = ''

            # Write the source clause.
            # Will not error if omitted. Maybe not the best plan.
            try:
                d = dict(name=ifAttributes['name'], inet=inet_val, source=ifAttributes['source'])
                interfaces.write(self.IFACE.substitute(d))
            except KeyError:
                pass

            # Write the addressing information.
            for field in self.addressFields:
                try:
                    d = dict(varient=field, value=ifAttributes[field])
                    interfaces.write(self.CMD.substitute(d))
                # Keep going if a field isn't provided.
                except KeyError:
                    pass

            # Write the bridge information.
            for field in self.bridgeFields:
                try:
                    d = dict(varient="bridge_" + field, value=ifAttributes['bridge-opts'][field])
                    interfaces.write(self.CMD.substitute(d))
                # Keep going if a field isn't provided.
                except KeyError:
                    pass

            # Write the up, down, pre-up, and post-down clauses.
            for field in self.prepFields:
                for item in ifAttributes[field]:
                    try:
                        d = dict(varient=field, value=item)
                        interfaces.write(self.CMD.substitute(d))
                    # Keep going if a field isn't provided.
                    except KeyError:
                        pass

    # Set up the interfaces object.
    def __init__(self):
        self.adapters = self.parseInterfaces()

        # Define templetes for blocks used in /etc/network/interfaces.
        from string import Template

        self.AUTO = Template('auto $name\n')
        self.HOTPLUG = Template('allow-hotplug $name\n')
        self.IFACE = Template('iface $name $inet $source\n')
        self.CMD = Template('\t$varient $value\n')

        self.addressFields = ['address', 'network', 'netmask', 'broadcast', 'gateway']
        self.prepFields = ['pre-up', 'up', 'down', 'post-down']
        self.bridgeFields = ['ports', 'fd', 'hello', 'maxage', 'stp']
