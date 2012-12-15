#Debinterface

This is a simple Python library for dealing with the /etc/network/interfaces file in most Debian based distributions.

## Changelog: 
1.0 - Dec 15 2012

	Read, writing, and editing supported.
	
	Specify file locations in constants.py


## Example useage:

    import debinterface
    
    # Get a collection of objects representing the network adapters.
    adapters = debinterface.interfaces()

    # You get a list you can iterare over.
    # Each adapter has an 'export()' method that returns a dictionary of its options.

    # You can print the name of each adapter as follows:
    for adapter in adapters:
    	item = adapter.export()
    	print(item['name'])
    
    # Write your new interfaces file as follows:
    # Any changes made with setter methods will be reflected with the new write.
    adapters.writeInterfaces()

    # A backup of your old interfaces file will be generated at the location
    # specified in constants.py (Default '/etc/network/interfaces.old')
