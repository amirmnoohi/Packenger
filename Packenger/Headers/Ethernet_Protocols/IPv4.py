from struct import *
import socket


class IPv4:
    def __init__(self, version, IHL, DSCP, ECN, length, identification, flags, offset, ttl, protocol, checksum, srcip,
                 dstip):
        self.version = version
        self.ihl = IHL
        self.dscp = DSCP
        self.ecn = ECN
        self.total_length = length
        self.identification = identification
        self.flags = flags
        self.fragment_offset = offset
        self.time_to_live = ttl
        self.protocol = protocol
        self.header_checksum = checksum
        self.source_ip_address = srcip
        self.destination_ip_address = dstip
        self.param = [self.version,
                      self.ihl,
                      self.dscp,
                      self.ecn,
                      self.total_length,
                      self.identification,
                      self.flags,
                      self.fragment_offset,
                      self.time_to_live,
                      self.protocol,
                      self.header_checksum,
                      socket.inet_ntoa(self.source_ip_address),
                      socket.inet_ntoa(self.destination_ip_address)]

        self.pkt = pack('!BBHHHBBH4s4s',
                        (self.version << 4) + self.ihl,
                        (self.dscp << 2) + self.ecn,
                        self.total_length,
                        self.identification,
                        self.flags << 13 + self.fragment_offset,
                        self.time_to_live,
                        self.protocol,
                        self.header_checksum,
                        self.source_ip_address,
                        self.destination_ip_address)

    def __str__(self):
        return self.pkt

    @staticmethod
    def parse(header):
        data = list(unpack('!BBHHHBBH4s4s', header))
        return IPv4(data[0] >> 4, data[0] & (2 ** 4 - 1), data[1] >> 2, data[1] & (2 ** 2 - 1), data[2],
                    data[3], data[4] >> 13, data[4] & (2 ** 12 - 1),
                    data[5], data[6], data[7],
                    data[8],
                    data[9])

    @staticmethod
    def process(self, interface, packet, header, **headers):
        ipv4_header = IPv4.parse(header)
        headers['ipv4'] = ipv4_header
        if ipv4_header.protocol == 0x01:
            from IPv4_Protocols import ICMP
            setattr(self.__class__, "icmp_process", ICMP.process)
            self.icmp_process(interface, packet, packet.data_bytes[34:38], **headers)
