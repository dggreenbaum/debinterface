import socket
import toolutils


class DnsmasqRange(object):
    '''
        Basic dnsmasq conf of the more file which holds the ip ranges
        per interface.
        Made for handling very basic dhcp-range options
    '''

    def __init__(self, path, backup_path=None):
        self._config = {}
        self._path = path
        if not backup_path:
            self.backup_path = path + ".bak"
        else:
            self.backup_path = backup_path

    @property
    def config(self):
        return self._config

    def set(self, key, value):
        if key == "dhcp-range":
            if not "dhcp-range" in self._config:
                self._config["dhcp-range"] = []
            if isinstance(value, str):
                value = self._extract_range_info(value)
            self._config["dhcp-range"].append(value)
        else:
            self._config[str(key).strip()] = value

    def validate(self):
        try:
            for r in self._config["dhcp-range"]:
                required = ["interface", "start", "end", "lease_time"]
                for k in required:
                    if not k in r:
                        raise ValueError("Missing option : {}".format(k))
                socket.inet_aton(r["start"])
                socket.inet_aton(r["end"])
                if r["start"] > r["end"]:
                    raise ValueError("Start IP range must be before end IP")
        except KeyError:
            pass  # dhcp-range is not mandatory

    def get_itf_range(self, if_name):
        ''' If no if, return None '''
        if not "dhcp-range" in self._config:
            return None
        for v in self._config['dhcp-range']:
            if v["interface"] == if_name:
                return v

    def rm_itf_range(self, if_name):
        ''' Rm range info for the given if '''

        if "dhcp-range" in self._config:
            self._config['dhcp-range'][:] = [x for x in self._config['dhcp-range'] if x["interface"] == if_name]

    def set_defaults(self):
        ''' Defaults for my needs, you should probably override this one '''
        self._config = {
            'dhcp-range': [
                {'interface': 'wlan0', 'start': '10.1.10.11', 'end': '10.1.10.250', 'lease_time': '24h'},
                {'interface': 'eth1', 'start': '10.1.20.10', 'end': '10.1.20.250', 'lease_time': '24h'}
            ],
            'dhcp-leasefile': '/var/tmp/dnsmasq.leases'
        }

    def read(self, path=None):
        if path is None:
            path = self._path

        self._config = {}

        with open(path, "r") as dnsmasq:
            for line in dnsmasq:
                if line.startswith('#') is True:
                    continue
                else:
                    key, value = line.split("=")

                    if key and value:
                        self.set(key, value)

    def write(self, path=None):
        self.validate()

        if path is None:
            path = self._path

        self.backup()

        with toolutils.atomic_write(path) as dnsmasq:
            for k, v in self._config.iteritems():
                if k == "dhcp-range":
                    for r in v:
                        dnsmasq.write("dhcp-range=interface:{},{},{},{}\n".format(
                            r["interface"], r["start"], r["end"], r["lease_time"]
                        ))
                else:
                    dnsmasq.write("{}={}\n".format(str(k).strip(), str(v).strip()))

    def controlService(self, action):
        ''' return True/False, command output '''

        if action not in ["start", "stop", "restart"]:
            return False, "Invalid action"
        return toolutils.safe_subprocess(["/etc/init.d/dnsmasq", action])

    def backup(self):
        ''' return True/False, command output '''

        if self.backup_path:
            return toolutils.safe_subprocess(["cp", self._path, self.backup_path])

    def restore(self):
        ''' return True/False, command output '''

        if self.backup_path:
            return toolutils.safe_subprocess(["cp", self.backup_path, self._path])

    def delete(self):
        ''' return True/False, command output '''

        if self.backup_path:
            return toolutils.safe_subprocess(["rm", self._path])

    def _extract_range_info(self, value):
        ret = {}
        breaked = value.split(",")
        ret["interface"] = breaked[0].split(":")[1]
        ret["start"] = breaked[1]
        ret["end"] = breaked[2]
        ret["lease_time"] = breaked[3]
        return ret
