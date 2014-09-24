import socket


class NetworkAdapter:
    ''' A representation a network adapter. '''

    def validateIP(self, ip):
        '''
            Validate an IP Address
            Raise socket.error on invalid IP
            Works for subnet masks too.
        '''
        socket.inet_aton(ip)

    def setName(self, n):
        ''' Set the inet option of an interface. '''
        self.ifAttributes['name'] = n

    def setInet(self, i):
        ''' Set the inet option of an interface. '''
        self.ifAttributes['inet'] = i

    def setAddressSource(self, s):
        ''' Set the address source for an interface. '''
        self.ifAttributes['source'] = s

    def setAddress(self, a):
        ''' Set the ipaddress of an interface. '''

        self.validateIP(a)
        self.ifAttributes['address'] = a

    def setNetmask(self, m):
        ''' Set the netmask of an interface. '''

        self.validateIP(m)
        self.ifAttributes['netmask'] = m

    def setGateway(self, g):
        ''' Set the default gateway of an interface. '''

        self.validateIP(g)
        self.ifAttributes['gateway'] = g

    def setBroadcast(self, b):
        ''' Set the broadcast address of an interface. '''

        self.validateIP(b)
        self.ifAttributes['broadcast'] = b

    def setNetwork(self, w):
        ''' Set the network identifier of an interface.'''

        self.validateIP(w)
        self.ifAttributes['network'] = w

    def setAuto(self, t):
        ''' Set the option to autostart the interface. '''
        self.ifAttributes['auto'] = t

    def setHotplug(self, h):
        ''' Set the option to allow hotplug on the interface. '''
        self.ifAttributes['hotplug'] = h

    def setBropts(self, opts):
        '''
            Set or append the bridge options of an interface.
            This should be a dictionary mapping option names and values.
            In the interfaces file, options will have a 'bridge_' prefix.
        '''
        self.ifAttributes['bridge-opts'] = opts

    def replaceBropt(self, key, value):
        self.ifAttributes['bridge-opts'][key] = value

    def appendBropts(self, key, value):
        self.ifAttributes['bridge-opts'][key] = self.ifAttributes['bridge-opts'][key] + value

    def setUp(self, up):
        '''
            Set and add to the up commands for an interface.
            Takes a LIST of shell commands.
        '''
        self.ifAttributes['up'] = up

    def appendUp(self, cmd):
        self.ifAttributes['up'].append(cmd)

    def setDown(self, down):
        '''
            Set and add to the down commands for an interface.
            Takes a LIST of shell commands.
        '''
        self.ifAttributes['down'] = down

    def appendDown(self, cmd):
        self.ifAttributes['down'].append(cmd)

    def setPreUp(self, pre):
        '''
            Set and add to the pre-up commands for an interface.
            Takes a LIST of shell commands.
        '''
        self.ifAttributes['pre-up'] = pre

    def appendPreUp(self, cmd):
        self.ifAttributes['pre-up'].append(cmd)

    def setPostDown(self, post):
        '''
            Set and add to the post-down commands for an interface.
            Takes a LIST of shell commands.
        '''
        self.ifAttributes['post-down'] = post

    def appendPostDown(self, cmd):
        self.ifAttributes['post-down'].append(cmd)

    def export(self):
        ''' Return the ifAttributes data structure. '''
        return self.ifAttributes

    def display(self):
        ''' Display a (kind of) human readable representation of the adapter. '''
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
                print(key + ': ' + str(self.ifAttributes[key]))
        print('============')

    def __init__(self, options=None):
        # Initialize attribute storage structre.
        self.reset()
        self.set_options(options)

    def reset(self):
        ''' Initialize attribute storage structre. '''
        self.ifAttributes = {}
        self.ifAttributes['bridge-opts'] = {}
        self.ifAttributes['up'] = []
        self.ifAttributes['down'] = []
        self.ifAttributes['pre-up'] = []
        self.ifAttributes['post-down'] = []

    def set_options(self, options):
        ''' raise ValueError or socket.error on issue '''

        # Set the name of the interface.
        if isinstance(options, str):
            self.setName(options)

        # If a dictionary of options is provided, populate the adapter options.
        elif isinstance(options, dict):
            try:
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
                    # Don't let one stupid option ruin file
                    else:
                        self.reset()
                        raise ValueError("Unknown option : {}".format(key))
            except socket.error:
                self.reset()
                raise
        else:
            raise ValueError("No arguments given. Provide a name or options dict.")
