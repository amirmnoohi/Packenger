from struct import *


class ICMP:
    def __init__(self, type, code, checksum):
        self.type = type
        self.code = code
        self.checksum = checksum
        self.param = [self.type,
                      self.code,
                      self.checksum]

        self.pkt = pack('!BBH',
                        self.type,
                        self.code,
                        self.checksum
                        )

    def __str__(self):
        return self.pkt

    @staticmethod
    def parse(header):
        data = list(unpack('!bbH', header))
        return ICMP(data[0], data[1], data[2])

    @staticmethod
    def process(self, interface, packet, header, **headers):
        icmp_header = ICMP.parse(header)
        headers['icmp'] = icmp_header
        find_record = self.ARPTable.findHWAddress(headers['ethernet'].param[0])
        if find_record:
            self.interfaces[self.ARPTable.DATA[find_record]["Interface"]].packenger.send(packet.data_bytes)
            print("ICMP Forwarded Successfully")
