This is a simple Python library for dealing with the /etc/network/interfaces file in most Debian based distributions.

The read module parses the file and populates networkAdapter objects.

The write module writes a new file populated with information from provided networkAdapter objects.

Editing of an existing file is facilitated by using read and write in series.
