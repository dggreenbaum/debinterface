#! /usr/bin/python

# Provides methods for writing to /etc/network/interfaces.

# Define templetes for blocks used in /etc/network/interfaces.
from string import Template

AUTO = Template('auto $name\n')
HOTPLUG = Template('allow-hotplug $name\n')
IFACE = Templeate('iface $name $inet $source\n')
CMD = Template('\t$varient $value\n')

addressFeilds = ['address', 'network', 'netmask', 'broadcast', 'gateway']

def writeInterfaces(adapters):
	# Back up the old interfaces file.
	import subprocess
	subprocess.call(["mv", "/etc/network/interfaces", "/etc/network/interfaces.old"])
	
	# Prepare to write the new interfaces file.
	interfaces = open("/etc/network/interfaces", "a")
	
	# Loop through the provided networkAdaprers and write the new file.
	for adapter in adapters:
		# Get dict of details about the adapter.
		ifAttributes = adapter.export()
		
		# Write auto and allow-hotplug clauses if applicable.		
		if adapter.ifAttributes['auto'] == True:
			d = dict(name=ifAttributes['name'])
			interfaces.write(AUTO.substitute(d))
                if ifAttributes['hotplug'] == True:
                        d = dict(name=adapter.ifAttributes['name'])
                        interfaces.write(HOTPLUG.substitute(d))
		
		# Construct and write the iface declaration.
		# The inet clause needs a little more processing.
		if ifAttribute['inet'] == True:
			inet_val = 'inet'
		else:
			inet_val = ''
		d = dict(name=ifAttributes['name'], inet=inet_val, source=ifAttributes['source'])
		interfaces.write(IFACE.substitute(d))
		
		# Write the addressing information.
		for feild in addressFeilds:
			try:
				d = dict(varient=feild, value=ifAttributes[feild])
				interfaces.write(CMD.substitute(d))
			# Keep going if a feild isn't provided.
			except Keyerror:
				pass
