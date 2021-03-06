from ..schema import schema
from .base import OpenWrtConverter


class Switch(OpenWrtConverter):
    netjson_key = 'switch'
    intermediate_key = 'network'
    _uci_types = ['switch', 'switch_vlan', 'switch_port']
    _switch_schema = schema['properties']['switch']['items']
    _vlan_schema = schema['properties']['switch']['items']['properties']['vlan']['items']
    _port_schema = schema['properties']['switch']['items']['properties']['port']['items']

    def __init__(self, *args, **kwargs):
        super(Switch, self).__init__(*args, **kwargs)
        # instance attributes used during backward conversion
        self._vlan_counter = 0
        self._port_counter = 0
        self._switch_map = {}

    def to_intermediate_loop(self, block, result, index=None):
        switch_vlan = self.__intermediate_switch(block)
        result.setdefault('network', [])
        result['network'] += switch_vlan
        return result

    def __intermediate_switch(self, switch):
        switch.update({
            '.type': 'switch',
            '.name': switch.pop('id', None) or
                     switch['name'],
        })
        vlans = []
        if 'vlan' in switch:
            for i, vlan in enumerate(switch['vlan'], start=1):
                vlan.update({
                    '.type': 'switch_vlan',
                    '.name': vlan.pop('id', None) or
                             self.__get_vlan_name(switch['name'], i)
                })
                if 'vid' not in vlan:
                    vlan['vid'] = vlan['vlan']
                vlans.append(self.sorted_dict(vlan))
            del switch['vlan']

        ports = []
        if 'port' in switch:
            for i, port in enumerate(switch['port'], start=1):
                port.update({
                    '.type': 'switch_port',
                    '.name': port.pop('id', None) or
                             self.__get_port_name(switch['name'], i)
                })
                ports.append(self.sorted_dict(port))
            del switch['port']

        return [self.sorted_dict(switch)] + vlans + ports

    def __get_vlan_name(self, name, i):
        return '{0}_vlan{1}'.format(name, i)

    def __get_port_name(self, name, i):
        return '{0}_port{1}'.format(name, i)

    def to_netjson_loop(self, block, result, index):
        _name = block.pop('.name')
        _type = block.pop('.type')
        result.setdefault('switch', [])
        if _type == 'switch':
            self._vlan_counter = 0
            self._port_counter = 0
            # set id attribute only if name option
            # and UCI identifier differ
            if _name != block['name']:
                block['id'] = _name
            switch = self.type_cast(block, self._switch_schema)
            self._switch_map[switch['name']] = switch
            result['switch'].append(switch)
        elif _type == 'switch_vlan':
            self._vlan_counter += 1
            # set id attribute only if name option
            # and expected UCI identifier differ
            if _name != self.__get_vlan_name(block['device'], self._vlan_counter):
                block['id'] = _name
            vlan = self.type_cast(block, self._vlan_schema)
            vlan = self.__netjson_vid(vlan)
            # appends vlan to the corresponding switch
            self._switch_map[vlan['device']].setdefault('vlan', [])
            self._switch_map[vlan['device']]['vlan'].append(vlan)
        elif _type == 'switch_port':
            self._port_counter += 1
            # set id attribute only if name option
            # and expected UCI identifier differ
            if _name != self.__get_port_name(block['device'], self._port_counter):
                block['id'] = _name
            port = self.type_cast(block, self._vlan_schema)
            # appends port to the corresponding switch
            self._switch_map[port['device']].setdefault('port', [])
            self._switch_map[port['device']]['port'].append(port)
            pass
        return result

    def __netjson_vid(self, vlan):
        if 'vid' in vlan:
            vlan['vid'] = int(vlan['vid'])
            if vlan['vid'] == vlan['vlan']:
                del vlan['vid']
        else:
            vlan['vid'] = None
        return vlan
