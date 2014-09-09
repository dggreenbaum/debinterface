#! /usr/bin/python

# Write interface
import subprocess
from string import Template
import constants


class InterfacesWriter:
    # Set up the interfaces object.
    def __init__(self, adapters=[]):
        self.adapters = adapters

        # Define templetes for blocks used in /etc/network/interfaces.
        self.AUTO = Template('auto $name\n')
        self.HOTPLUG = Template('allow-hotplug $name\n')
        self.IFACE = Template('iface $name $inet $source\n')
        self.CMD = Template('\t$varient $value\n')

        self.addressFields = ['address', 'network', 'netmask', 'broadcast', 'gateway']
        self.prepFields = ['pre-up', 'up', 'down', 'post-down']
        self.bridgeFields = ['ports', 'fd', 'hello', 'maxage', 'stp']

    def backup_interfaces(self):
        subprocess.call(["mv", constants.INTERFACES, constants.BACKUP])

    def write_interfaces(self):

        # Back up the old interfaces file.
        self.backup_interfaces()

        # Prepare to write the new interfaces file.
        with open(constants.INTERFACES, "a") as interfaces:
            # Loop through the provided networkAdaprers and write the new file.
            for adapter in self.adapters:
                # Get dict of details about the adapter.
                ifAttributes = adapter.export()

                self._write_auto(interfaces, adapter, ifAttributes)
                self._write_hotplug(interfaces, adapter, ifAttributes)
                self._write_inet(interfaces, adapter, ifAttributes)
                self._write_addressing(interfaces, adapter, ifAttributes)
                self._write_bridge(interfaces, adapter, ifAttributes)
                self._write_callbacks(interfaces, adapter, ifAttributes)

    def _write_auto(self, interfaces, adapter, ifAttributes):
        ''' Write if applicable '''
        try:
            if adapter.ifAttributes['auto'] is True:
                d = dict(name=ifAttributes['name'])
                interfaces.write(self.AUTO.substitute(d))
        except KeyError:
            pass

    def _write_hotplug(self, interfaces, adapter, ifAttributes):
        ''' Write if applicable '''
        try:
            if ifAttributes['hotplug'] is True:
                d = dict(name=adapter.ifAttributes['name'])
                interfaces.write(self.HOTPLUG.substitute(d))
        except KeyError:
            pass

    def _write_inet(self, interfaces, adapter, ifAttributes):
        # Construct and write the iface declaration.
        # The inet clause needs a little more processing.
        if ifAttributes['inet'] is True:
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

    def _write_addressing(self, interfaces, adapter, ifAttributes):
        for field in self.addressFields:
            try:
                d = dict(varient=field, value=ifAttributes[field])
                interfaces.write(self.CMD.substitute(d))
            # Keep going if a field isn't provided.
            except KeyError:
                pass

    def _write_bridge(self, interfaces, adapter, ifAttributes):
        # Write the bridge information.
        for field in self.bridgeFields:
            try:
                d = dict(varient="bridge_" + field, value=ifAttributes['bridge-opts'][field])
                interfaces.write(self.CMD.substitute(d))
            # Keep going if a field isn't provided.
            except KeyError:
                pass

    def _write_callbacks(self, interfaces, adapter, ifAttributes):
        # Write the up, down, pre-up, and post-down clauses.
        for field in self.prepFields:
            for item in ifAttributes[field]:
                try:
                    d = dict(varient=field, value=item)
                    interfaces.write(self.CMD.substitute(d))
                # Keep going if a field isn't provided.
                except KeyError:
                    pass
