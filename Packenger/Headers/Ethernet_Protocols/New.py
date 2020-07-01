from struct import *


class New:
    def __init__(self, protocol, y, x):
        self.protocol = protocol
        self.y = y
        self.x = x
        self.param = [
            self.protocol,
            self.y,
            self.x
        ]

        self.pkt = pack('!B6s8s',
                        self.protocol,
                        self.y,
                        self.x
                        )

    def __str__(self):
        return self.pkt

    @staticmethod
    def parse(header):
        data = list(unpack('!B6s8s', header))
        return New(data[0], data[1], data[2])

    @staticmethod
    def process(self, interface, packet, header, **headers):
        new_header = New.parse(header)
        headers['new'] = new_header
        print(headers)
