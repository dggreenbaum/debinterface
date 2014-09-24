# Write interface
from string import Template
import constants
import tools


class InterfacesWriter:
    ''' Short lived class to write interfaces file '''

    # Define templetes for blocks used in /etc/network/interfaces.
    _auto = Template('auto $name\n')
    _hotplug = Template('allow-hotplug $name\n')
    _iface = Template('iface $name $inet $source\n')
    _cmd = Template('\t$varient $value\n')

    _addressFields = ['address', 'network', 'netmask', 'broadcast', 'gateway']
    _prepFields = ['pre-up', 'up', 'down', 'post-down']
    _bridgeFields = ['ports', 'fd', 'hello', 'maxage', 'stp']

    def __init__(self, adapters=[]):
        self._adapters = adapters

    @property
    def adapters(self):
        return self._adapters

    @adapters.setter
    def adapters(self, value):
        self._adapters = value

    def backup_interfaces(self):
        ''' return True/False, command output '''

        return tools.safe_subprocess(["mv", constants.INTERFACES, constants.BACKUP])

    def write_interfaces(self):
        # Back up the old interfaces file.
        self.backup_interfaces()

        # Prepare to write the new interfaces file.
        with open(constants.INTERFACES, "a") as interfaces:
            # Loop through the provided networkAdaprers and write the new file.
            for adapter in self._adapters:
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
                interfaces.write(self._auto.substitute(d))
        except KeyError:
            pass

    def _write_hotplug(self, interfaces, adapter, ifAttributes):
        ''' Write if applicable '''
        try:
            if ifAttributes['hotplug'] is True:
                d = dict(name=adapter.ifAttributes['name'])
                interfaces.write(self._hotplug.substitute(d))
        except KeyError:
            pass

    def _write_inet(self, interfaces, adapter, ifAttributes):
        ''' Construct and write the iface declaration.
            The inet clause needs a little more processing.
        '''
        if ifAttributes['inet'] is True:
            inet_val = 'inet'
        else:
            inet_val = ''

        # Write the source clause.
        # Will not error if omitted. Maybe not the best plan.
        try:
            d = dict(name=ifAttributes['name'], inet=inet_val, source=ifAttributes['source'])
            interfaces.write(self._iface.substitute(d))
        except KeyError:
            pass

    def _write_addressing(self, interfaces, adapter, ifAttributes):
        for field in self._addressFields:
            try:
                d = dict(varient=field, value=ifAttributes[field])
                interfaces.write(self._cmd.substitute(d))
            # Keep going if a field isn't provided.
            except KeyError:
                pass

    def _write_bridge(self, interfaces, adapter, ifAttributes):
        ''' Write the bridge information. '''
        for field in self._bridgeFields:
            try:
                d = dict(varient="bridge_" + field, value=ifAttributes['bridge-opts'][field])
                interfaces.write(self._cmd.substitute(d))
            # Keep going if a field isn't provided.
            except KeyError:
                pass

    def _write_callbacks(self, interfaces, adapter, ifAttributes):
        ''' Write the up, down, pre-up, and post-down clauses. '''
        for field in self._prepFields:
            for item in ifAttributes[field]:
                try:
                    d = dict(varient=field, value=item)
                    interfaces.write(self._cmd.substitute(d))
                # Keep going if a field isn't provided.
                except KeyError:
                    pass
