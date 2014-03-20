#! /usr/bin/python

# A representation a network adapter.
class networkAdapter:
    #Validate an IP Address
    # Will return 0 on fail, 1 on success.
    # Works for subnet masks too.
    def validateIP(self, ip):
        import socket
        try:
            socket.inet_aton(ip)
        except socket.error:
            return 0
        return 1

    # Set the inet option of an interface.
    def setName(self, n):
        self.ifAttributes['name'] = n

    # Set the inet option of an interface.
    def setInet(self, i):
        self.ifAttributes['inet'] = i

    # Set the address source for an interface.
    def setAddressSource(self, s):
        self.ifAttributes['source'] = s

    # Set the ipaddress of an interface.
    def setAddress(self, a):
        if self.validateIP(a) == 1:
            self.ifAttributes['address'] = a
        else:
            pass

    # Set the netmask of an interface.
    def setNetmask(self, m):
        if self.validateIP(m) == 1:
            self.ifAttributes['netmask'] = m
        else:
            pass

    # Set the default gateway of an interface.
    def setGateway(self, g):
        if self.validateIP(g) == 1:
            self.ifAttributes['gateway'] = g
        else:
            pass

    # Set the broadcast address of an interface.
    def setBroadcast(self, b):
        if self.validateIP(b) == 1:
            self.ifAttributes['broadcast'] = b
        else:
            pass

    # Set the network identifier of an interface.
    def setNetwork(self, w):
        if self.validateIP(w) == 1:
            self.ifAttributes['network'] = w
        else:
            pass

    # Set the option to autostart the interface.
    def setAuto(self, t):
        self.ifAttributes['auto'] = t

    # Set the option to allow hotplug on the interface.
    def setHotplug(self, h):
        self.ifAttributes['hotplug'] = h

    # Set or append the bridge options of an interface.
    # This should be a dictionary mapping option names and values.
    # In the interfaces file, options will have a 'bridge_' prefix.
    def setBropts(self, opts):
        self.ifAttributes['bridge-opts'] = opts

    def replaceBropt(self, key, value):
        self.ifAttributes['bridge-opts'][key] = value

    def appendBropts(self, key, value):
        self.ifAttributes['bridge-opts'][key] = self.ifAttributes['bridge-opts'][key] + value

    # Set and add to the up commands for an interface.
    # Takes a LIST of shell commands.
    def setUp(self, up):
        self.ifAttributes['up'] = up
    def appendUp(self, cmd):
        self.ifAttributes['up'].append(cmd)

    # Set and add to the down commands for an interface.
    # Takes a LIST of shell commands.
    def setDown(self, down):
            self.ifAttributes['down'] = down
    def appendDown(self, cmd):
            self.ifAttributes['down'].append(cmd)

    # Set and add to the pre-up commands for an interface.
    # Takes a LIST of shell commands.
    def setPreUp(self, pre):
            self.ifAttributes['pre-up'] = pre
    def appendPreUp(self, cmd):
            self.ifAttributes['pre-up'].append(cmd)

    # Set and add to the post-down commands for an interface.
    # Takes a LIST of shell commands.
    def setPostDown(self, post):
            self.ifAttributes['post-down'] = post
    def appendPostDown(self, cmd):
            self.ifAttributes['post-down'].append(cmd)

    # Return the ifAttributes data structure.
    def export(self):
        return self.ifAttributes

    # Display a (kind of) human readable representation of the adapter.
    def display(self):
        print('============')
        for key in self.ifAttributes.keys():
            if isinstance(self.ifAttributes[key], list):
                print(key + ': ')
                for item in self.ifAttributes[key]:
                    print('\t' + item)

            elif isinstance(self.ifAttributes[key], dict):
                print(key + ': ')
                for item in self.ifAttributes[key].keys():
                    print('\t' + item + ': ' + self.ifAttributes[key][item])
            else:
                print(key + ': ' +str(self.ifAttributes[key]))
        print('============')

        # Set up the network adapter.
    def __init__(self, options=None):
        # Initialize attribute storage structre.
        self.ifAttributes = {}
        self.ifAttributes['bridge-opts'] = {}
        self.ifAttributes['up'] = []
        self.ifAttributes['down'] = []
        self.ifAttributes['pre-up'] = []
        self.ifAttributes['post-down'] = []

        # Set the name of the interface.
        if isinstance(options, str):
            self.setName(options)

        # If a dictionary of options is provided, populate the adapter options.
        elif isinstance(options, dict):
            for key in options.keys():
                if key == 'name':
                    self.setName(options[key])
                if key == 'inet':
                    self.setInet(options[key])
                elif key == 'source':
                    self.setAddressSource(options[key])
                elif key == 'address':
                    self.setAddress(options[key])
                elif key == 'netmask':
                    self.setNetmask(options[key])
                elif key == 'gateway':
                    self.setGateway(options[key])
                elif key == 'broadcast':
                    self.setBroadcast(options[key])
                elif key == 'network':
                    self.setNetwork(options[key])
                elif key == 'auto':
                    self.setAuto(options[key])
                elif key == 'allow-hotplug':
                    self.setHotplug(options[key])
                elif key == 'bridgeOpts':
                    self.setBropts(options[key])
                elif key == 'up':
                    self.setUp(options[key])
                elif key == 'down':
                    self.setDown(options[key])
                elif key == 'pre-up':
                    self.setPreUp(options[key])
                elif key == 'post-down':
                    self.setPostDown(options[key])
                # Don't let one stupid option ruin everyone's day.
                else:
                    pass
        else:
            print("No arguments given. Provide a name or options dict.")
