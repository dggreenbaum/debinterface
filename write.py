#! /usr/bin/python

# Provides methods for writing to /etc/network/interfaces.

# Define templetes for blocks used in /etc/network/interfaces.
from string import Template

AUTO = Template('auto $name\n')
HOTPLUG = Template('allow-hotplug $name\n')
IFACE = Template('iface $name $inet $source\n')
CMD = Template('\t$varient $value\n')

addressFields = ['address', 'network', 'netmask', 'broadcast', 'gateway']
prepFields =['pre-up', 'up', 'down', 'post-down']

# Get constants.
import constants

def writeInterfaces(adapters):
	# Back up the old interfaces file.
	import subprocess
	subprocess.call(["mv", constants.INTERFACES, constants.BACKUP])
	
	# Prepare to write the new interfaces file.
	interfaces = open(constants.INTERFACES, "a")
	
	# Loop through the provided networkAdaprers and write the new file.
	for adapter in adapters:
		# Get dict of details about the adapter.
		ifAttributes = adapter.export()
		
		# Write auto and allow-hotplug clauses if applicable.		
		try:
			if adapter.ifAttributes['auto'] == True:
				d = dict(name=ifAttributes['name'])
				interfaces.write(AUTO.substitute(d))
                except KeyError:
			pass
		
		try:
			if ifAttributes['hotplug'] == True:
                        	d = dict(name=adapter.ifAttributes['name'])
                        	interfaces.write(HOTPLUG.substitute(d))
		except KeyError:
			pass
		
		# Construct and write the iface declaration.
		# The inet clause needs a little more processing.
		if ifAttributes['inet'] == True:
			inet_val = 'inet'
		else:
			inet_val = ''
		d = dict(name=ifAttributes['name'], inet=inet_val, source=ifAttributes['source'])
		interfaces.write(IFACE.substitute(d))
		
		# Write the addressing information.
		for field in addressFields:
			try:
				d = dict(varient=field, value=ifAttributes[field])
				interfaces.write(CMD.substitute(d))
			# Keep going if a field isn't provided.
			except KeyError:
				pass
		
		# Write the up, down, pre-up, and post-down clauses.
		for field in prepFields:
			for item in ifAttributes[field]:
				try:
                                	d = dict(varient=field, value=item)
                                	interfaces.write(CMD.substitute(d))
                        	# Keep going if a field isn't provided.
                        	except Keyerror:
                                	pass
