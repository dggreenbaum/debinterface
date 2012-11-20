#! /usr/bin/python

# Provides methods for the reading of /etc/network/interfaces.
# Allows the settings stored within to be used in other Python modules.

from adapter import networkAdapter

# Read /etc/network/interfaces.
# Return an array of networkAdapter instances.
def parseInterfaces():
	# Open up the interfaces file. Read only.
	interfaces = open("/etc/network/interfaces.test", "r")
	
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
						adapters[context].appendBropts(opt[1], sline[1])
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
# TESTING
#adapters = parseInterfaces()
#for adapter in adapters:
#	adapter.display()
