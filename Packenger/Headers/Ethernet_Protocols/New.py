from struct import *


class New:
    def __init__(self, y, x, protocol):
        self.y = y
        self.x = x
        self.protocol = protocol
        self.param = [
            self.y,
            self.x,
            self.protocol
        ]

        self.pkt = pack('!8s8sB',
                        self.y,
                        self.x,
                        self.protocol
                        )

    def __str__(self):
        return self.pkt

    @staticmethod
    def parse(header):
        data = list(unpack('!8s8sB', header))
        return New(data[0], data[1], data[2])

    @staticmethod
    def process(self, interface, packet, header, **headers):
        new_header = New.parse(header)
        headers['new'] = new_header
        print(headers)
