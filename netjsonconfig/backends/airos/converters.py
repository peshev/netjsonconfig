from ...utils import get_copy, sorted_dict
from ..base.converter import BaseConverter


class Aaa(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append([
            {
                'radius': {
                    'acct': [
                        {
                            'port': 1813,
                            'status': 'disabled',
                        },
                    ],
                    'auth': [
                        {
                            'port': 1812,
                        },
                    ],
                },
                'status': 'disabled',
            }
        ])
        return (('aaa', result),)

class Bridge(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        original = [
                i for i in get_copy(self.netjson, self.netjson_key) if i['type'] == 'bridge'
                ]

        bridges = []
        for interface in original:
            bridge_ports = []
            for port in interface.get('bridge_members',[]):
                bridge_ports.append({
                    'devname' : port,
                    'status' : 'enabled',
                })

            bridges.append({
                'comment' : interface.get('comment', ''),
                'devname' : interface['name'],
                'port' : bridge_ports,
            })


        result.append(bridges)
        result.append({
            'status': 'enabled',
        })

        return (('bridge', result),)


class Discovery(BaseConverter):
    netjson_key = 'general'

class Gui(BaseConverter):
    netjson_key = 'gui'

    def to_intermediate(self):
        result = [
                {
                    'language': 'it_IT',
                },
                {
                    'network' : {
                        'advanced' : {
                            'status' : 'enabled',
                        }
                    }
                }
        ]
        return (('gui', result),)


class Httpd(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
                {
                    'https' : {
                        'port' : 443,
                        'status' : 'enabled',
                    },
                },
                {
                    'port' : 80,
                    'session' : {
                        'timeout' : 900,
                    },
                    'status': 'enabled',
                },
        ]

        return (('httpd', result),)


class Netconf(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        interfaces = []
        original = [
                i for i in get_copy(self.netjson, self.netjson_key)
                ]

        for interface in original:

            interfaces.append({
                'devname':  interface['name'],
                'status':  'disabled' if interface.get('disabled', False) else 'enabled',
            })

        result.append(interfaces)
        result.append({
            'status':  'enabled',
        })
        return (('netconf', result),)


class Netmode(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []

        result.append({
            'status': 'enabled',
        })
        return (('netmode', result), )


class Ntpclient(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'status': 'enabled',
        })
        return (('ntpclient',result),)



class Pwdog(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'delay': 300,
            'period': 300,
            'retry': 3,
            'status': 'enabled',
        })
        return (('pwdog', result),)


class Radio(BaseConverter):
    netjson_key = 'radios'

    def to_intermediate(self):
        result = []

        original = get_copyt(self.netjson, self.netjson_key)

        radios = []

        for r in original:
            radios.append({
                'devname': r['name'],
                'status': 'enabled',
                'txpower': r.get('tx_power',''),
            })

        result.append({
            'status': 'enabled',
        })

        return (('radio', result),)


class Resolv(BaseConverter):
    netjson_key = 'dns_servers'

    def to_intermediate(self):
        result = []

        result.append({
            'host':  [{
                'name':  ''
            }]
        })

        original = get_copy(self.netjson, self.netjson_key)

        a = {
                'nameserver':  [],
        }
        for nameserver in original:
            a['nameserver'].append({
                'ip':  nameserver,
                'status':  'enabled',
            })

        result.append(a)

        result.append({
            'status':  'enabled',
        })

        return (('resolv', result),)


class Route(BaseConverter):
    netjson_key = 'routes'

    def to_intermediate(self):
        result = []
        original = get_copy(self.netjson, self.netjson_key)

        routes = []

        for r in original:
            routes.append({
                'devname': '',
                'gateway': '0.0.0.0',
                'ip': '0.0.0.0',
                'netmask': 0,
                'status': 'enabled',
            })

        result.append(routes)

        result.append({
            'status': 'enabled',
        })
        return (('route', result),)


class Snmp(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = [
               {
                    'community':  'public',
                    'contact':  'value',
                    'location':  '',
                    'status':  'enabled',
                },
        ]

        return (('snmp', result),)


class Sshd(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'port': 22,
            'status': 'enabled',
        })
        return (('sshd', result),)

class Syslog(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'status': 'disabled',
        })
        return (('syslog', result),)


class System(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        return (('system', result),)


class Telnetd(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'port': 23,
            'status': 'enabled',
        })
        return (('telnetd', result),)


class Update(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'check': {
                'status': 'enabled',
            },
        })
        return (('update', result),)


class Users(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'status': 'enabled',
        })

        result.append([
            {
                'name': 'root',
                'password': 'changeme',
                'status': 'enabled',
            },
        ])

        return (('users', result),)


class Vlan(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        original = [
                i for i in get_copy(self.netjson, self.netjson_key) if '.' in i['name']
                ]

        vlans = []
        for v in original:
            vlans.append({
                'comment' : v.get('comment', ''),
                'devname' : v['name'].split('.')[0],
                'id' : v['name'].split('.')[1],
                'status' : 'disabled' if v['disabled'] else 'enabled',
            })

        result.append(vlans)
        result.append({
            'status': 'enabled',
        })

        return (('vlan', result),)


class Wireless(BaseConverter):
    netjson_key = 'interfaces'

    def to_intermediate(self):
        result = []
        original = [
                i for i in get_copy(self.netjson, self.netjson_key) if hasattr(i,'wireless')
                ]

        ws = []
        for w in original:
            hide_ssid = 'enabled' if w['wireless']['hide_ssid'] else 'disabled'
            encryption = w['wireless'].get('encryption', 'none')
            ws.append({
                'addmtikie': 'enabled',
                'devname' : w['name'],
                'hide_ssid' : hide_ssid,
                'security' : { 'type' : encryption },
                'ssid' : w['wireless']['ssid'],
                'status' : 'enabled',
                'wds' : { 'status': 'enabled' },
            })
        result.append(ws)

        result.append({
            'status': 'enabled',
        })

        return (('wireless', result),)

class Wpasupplicant(BaseConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []

        result.append({
            'device': [
                {
                    'status': 'disabled',
                },
            ],
            'profile': [
                {
                    'network': [
                        {
                            'ssid': 'your-ssid-here',
                        },
                    ],
                },
            ],
        })
        return (('wpasupplicant', result),)