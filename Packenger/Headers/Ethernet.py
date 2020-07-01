from struct import *


class Ethernet:
    def __init__(self, dstmac, srcmac, type):
        """
        e.g : Ethernet("\xAA\xAA\xAA\xAA\xAA\xAA", "\xAA\xAA\xAA\xAA\xAA\xAA", 0x0450)
        :param dstmac : Destination mac address:
        :param srcmac  : Source mac address:
        :param type : Ethernet Type:
        """
        self.destination_mac_address = dstmac
        self.source_mac_address = srcmac
        self.ether_type = type
        self.param = [self.convert_mac(self.destination_mac_address),
                      self.convert_mac(self.source_mac_address),
                      self.ether_type]
        self.pkt = pack('!6s6sH',
                        self.destination_mac_address,
                        self.source_mac_address,
                        self.ether_type)

    @staticmethod
    def convert_mac(bytes_mac):
        bytes_str = map('{:02x}'.format, list(ord(x) for x in (list(bytes_mac))))
        return ':'.join(bytes_str).upper()

    def __str__(self):
        return self.pkt

    @staticmethod
    def parse(header):
        data = list(unpack('!6s6sH', header[:14]))
        return Ethernet(data[0], data[1], data[2])

    @staticmethod
    def process(self, interface, packet, header):
        ethernet_header = Ethernet.parse(header)
        headers = {'ethernet': ethernet_header}
        if ethernet_header.ether_type == 0x0806:
            from Ethernet_Protocols import ARP
            setattr(self.__class__, "arp_process", ARP.process)
            self.arp_process(interface, packet, packet.data_bytes[14:42])
        elif ethernet_header.ether_type == 0x0800:
            from Ethernet_Protocols import IPv4
            setattr(self.__class__, "ipv4_process", IPv4.process)
            self.ipv4_process(interface, packet, packet.data_bytes[14:34], **headers)
        elif ethernet_header.ether_type == 0x0801:
            from Ethernet_Protocols import New
            setattr(self.__class__, "new_process", New.process)
            self.new_process(interface, packet, packet.data_bytes[14:34], **headers)
        else:
            print("Malformed Packet")
