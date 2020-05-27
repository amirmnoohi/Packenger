import netmap

from Packet import Packet


class Packenger:
    def __init__(self, interface):
        self.txr = None
        self.receive_queue_length = 0
        self.receive_queue = list()
        self.listen_thread = None  # for listen on interface in parallel
        self.interface = interface
        self._stop_listen = False
        self._netmap = netmap.NetmapDesc('netmap:' + interface)
        self._txr = self._netmap.transmit_rings[0]
        self._rxr = self._netmap.receive_rings[0]
        self._txr_cur = self._txr.cur
        self._rxr_cur = self._rxr.cur
        self._txr_num_slots = self._txr.num_slots
        self._rxr_num_slots = self._rxr.num_slots

    def send(self, packet):
        self._txr.slots[self._txr_cur].buf[0:len(packet)] = packet
        self._txr.slots[self._txr_cur].len = len(packet)
        self._txr_cur += 1
        if self._txr_cur >= self._txr.num_slots:
            self._txr_cur -= self._txr.num_slots
        self._txr.cur = self._txr.head = self._txr_cur  # lazy update txr.cur and txr.head
        self._netmap.txsync()

    def listen(self, packet_processor=None):
        while not self._stop_listen:
            # sync RX rings with kernel
            self._netmap.rxsync()

            # scan all the receive rings
            rxr = None
            for i in range(self._netmap.interface.rx_rings):
                if self._netmap.receive_rings[i].head != self._netmap.receive_rings[i].tail:
                    # At least one packet has been received on
                    # this ring
                    rxr = self._netmap.receive_rings[i]
                    break

            if rxr is None:
                # no packets received on the rings, let's sleep a bit
                # time.sleep(1)
                continue

            # slot pointed by rxr.head has been received
            # and can be extracted
            slot = rxr.slots[rxr.head]

            # convert the buffer associated to the slot to
            # a string of hexadecimal digits, up to the received length
            self.receive_queue.append(Packet(slot.buf[:slot.len].tobytes(),
                                             slot.buf[:slot.len].tolist(),
                                             slot.len))
            self.receive_queue_length += 1

            if packet_processor:
                packet_processor(self.interface, self.receive_queue[-1])

            # update head and cur, managing index wraparound
            rxr.head = rxr.head + 1
            if rxr.head >= rxr.num_slots:
                rxr.head -= rxr.num_slots
            rxr.cur = rxr.head

    def stop_listen(self):
        self._stop_listen = True
