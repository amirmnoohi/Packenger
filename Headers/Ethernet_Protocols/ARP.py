from struct import *
import socket
import binascii


class ARP:
    def __init__(self, sha, spa, tha, tpa, htype=0x1, ptype=0x0800, hlen=0x6, plen=0x4, oper=0x2):
        self.htype = htype
        self.ptype = ptype
        self.hlen = hlen
        self.plen = plen
        self.oper = oper
        self.sha = sha
        self.spa = spa
        self.tha = tha
        self.tpa = tpa
        self.param = [self.htype,
                      hex(self.ptype),
                      self.hlen,
                      self.plen,
                      self.oper,
                      self.convert_mac(self.sha),
                      socket.inet_ntoa(self.spa),
                      self.convert_mac(self.tha),
                      socket.inet_ntoa(self.tpa)]
        self.pkt = pack('!HHBBH6s4s6s4s',
                        self.htype,
                        self.ptype,
                        self.hlen,
                        self.plen,
                        self.oper,
                        self.sha,
                        self.spa,
                        self.tha,
                        self.tpa
                        )

    @staticmethod
    def convert_mac(bytes_mac):
        bytes_str = map('{:02x}'.format, list(ord(x) for x in (list(bytes_mac))))
        return ':'.join(bytes_str).upper()

    def __str__(self):
        return self.pkt

    @staticmethod
    def parse(header):
        data = list(unpack('!HHBBH6s4s6s4s', header))
        return ARP(data[5], data[6], data[7], data[8], data[0], data[1], data[2], data[3], data[4])

    @staticmethod
    def process(self, interface, packet, header, **headers):
        arp_header = ARP.parse(header)
        if arp_header.oper == 0x1:
            find_record = self.ARPTable.findIPAddress(arp_header.param[8])
            if find_record:
                from Packenger import Ethernet
                pkt = str(
                    Ethernet(arp_header.sha,
                             binascii.unhexlify(self.interfaces[interface].NETLINK["addr"].replace(':', '')),
                             0x0806))
                pkt += str(ARP(binascii.unhexlify(self.ARPTable.DATA[find_record]["HWAddress"].replace(':', '')),
                               arp_header.tpa,
                               arp_header.sha,
                               arp_header.spa,
                               oper=0x2))
                self.interfaces[interface].packenger.send(pkt)
            print("ARP Not Found")
        if arp_header.oper == 0x2:
            print("\t\t\t\tResponse ARP")
