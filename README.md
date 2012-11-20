#Debinterface

This is a simple Python library for dealing with the /etc/network/interfaces file in most Debian based distributions.

## Status: 
Parsing the interfaces file works pretty well at this stage.
Writing to the file is not quite complete yet and untested.


Example useage:

    import debinterface
    
    # Get a collectionf of objects representing the network adapters.
    adapters = debinterface.read.parseInterfaces()

    # You get a list you can iterare over.
    # Each adapter has an 'export()' method that returns a dictionary of its options.

    # You can print the name of each adapter as follows:
    for adapter in adapters:
	print(adapter.export()['name'])
