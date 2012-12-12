#Debinterface

This is a simple Python library for dealing with the /etc/network/interfaces file in most Debian based distributions.

## Status: 
Parsing the interfaces file works pretty well at this stage.
Writing to the file is working and needs to be integrated into the interfaces class.


## Example useage:

    import debinterface
    
    # Get a collectionf of objects representing the network adapters.
    adapters = debinterface.interfaces()

    # You get a list you can iterare over.
    # Each adapter has an 'export()' method that returns a dictionary of its options.

    # You can print the name of each adapter as follows:
    for adapter in adapters:
    	item = adapter.export()
    	print(item['name'])
