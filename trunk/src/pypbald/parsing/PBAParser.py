'''
    PBAParser class

    It parses filtered broadcast packets and encapsulates them in well formed
    records

    Implements two type of records:
    - ARP
    - NBDS

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"

import time
import dpkt
import dpkt.netbios
from dpkt.ethernet import Ethernet
from dpkt.arp import ARP
from binascii import hexlify
from pypbald.PBASingleton import PBASingleton
from pypbald.records.PBARecordNBDS import PBARecordNBDS
from pypbald.records.PBARecordARPRequest import PBARecordARPRequest

class PBAParser(PBASingleton):
    '''
        PBAParser
        
        This class:
        - receives filtered broadcast packets
        - make a straigth classification of them
        - extract well formed record from them

        It is implemented as a Singleton Pattern
    '''
    _pba = None
    _packet = None

    def __init__(self, pba):
        '''
            PBAParser constructor
        '''
        self._pba = pba

    def extract_nbds(self, packet, timestamp, interface_name=None):
        '''
            Extracts NBDS record from a packet
        '''
        raw_packet = packet
        ethernet_frame = Ethernet(raw_packet)
        ethernet_data = ethernet_frame.data
        udp_packet = ethernet_data.data
        src_mac = hexlify(ethernet_frame['src']).decode('ascii')
        src_ip = hexlify(ethernet_data['src']).decode('ascii')
        dst_ip = hexlify(ethernet_data['dst']).decode('ascii')
        srcip = str(int(src_ip[0:2], 16))
        srcip = srcip + '.' + str(int(src_ip[2:4], 16))
        srcip = srcip + '.' + str(int(src_ip[4:6], 16))
        srcip = srcip + '.' + str(int(src_ip[6:8], 16))
        dstip = str(int(dst_ip[0:2], 16))
        dstip = dstip + '.' + str(int(dst_ip[2:4], 16))
        dstip = dstip + '.' + str(int(dst_ip[4:6], 16))
        dstip = dstip + '.' + str(int(dst_ip[6:8], 16))
        offset = 0
        snn1 = 15 + offset
        snn2 = 47 + offset
        thetime = time.strftime("%Y%m%d%H%M%S", time.gmtime(timestamp))
        nbname = dpkt.netbios.decode_name(udp_packet.data[snn1:snn2])
        snbname = udp_packet.data[snn1:snn2]
        hnbname = hexlify(udp_packet.data[snn1:snn2]).decode('ascii')
        dnn1 = 49 + offset
        dnn2 = 81 + offset
        dnbname = dpkt.netbios.decode_name(udp_packet.data[dnn1:dnn2])
        sdnbname = udp_packet.data[dnn1:dnn2]
        hdnbname = hexlify(udp_packet.data[dnn1:dnn2]).decode('ascii')
        if (self._pba.cfg('debug')):
            print(hexlify(udp_packet.data).decode('ascii'))
            print(hexlify(udp_packet.data[0:14]).decode('ascii'))
            print(hexlify(udp_packet.data[snn1:snn2]).decode('ascii'))
            print(hexlify(udp_packet.data[dnn1:dnn2]).decode('ascii'))
            print(nbname)
            print(dnbname)
            print(snbname)
            print(sdnbname)

        record = PBARecordNBDS(raw_packet, timestamp, interface_name)
        record.assign(thetime,
                      src_mac,
                      srcip,
                      dstip,
                      nbname,
                      hnbname,
                      snbname[0:30],
                      dnbname,
                      hdnbname,
                      sdnbname[0:30])
        return record


    def extract_arp(self, packet, timestamp, interface_name=None):
        '''
            Extracts an ARP record from a packet
        '''
        raw_packet = packet
        ethernet_frame = Ethernet(raw_packet)
        thetime = time.strftime("%Y%m%d%H%M%S", time.gmtime(timestamp))
        arp = ethernet_frame.data
        src_mac = hexlify(arp.sha).decode('ascii')
        src_ip_encoded = hexlify(arp.spa).decode('ascii')
        dst_ip_encoded = hexlify(arp.tpa).decode('ascii')
        src_ip = '.'.join(str(int(i, 16)) for i in ([src_ip_encoded[i:i+2]
                    for i in range(0, len(src_ip_encoded), 2)]))
        dst_ip = '.'.join(str(int(i, 16)) for i in ([dst_ip_encoded[i:i+2]
                    for i in range(0, len(dst_ip_encoded), 2)]))
        if (self._pba.cfg('debug')):
            print(src_mac)
            print(src_ip)
            print(dst_ip)

        record = PBARecordARPRequest(raw_packet, timestamp, interface_name)
        record.assign(thetime,
                      src_mac,
                      src_ip)
        return record

    def parse(self, packet, timestamp, interface_name=None):
        '''
            It parses filtered broadcast packets and encapsulates them in well formed
            records

            Implements two type of records:
            - ARP
            - NBDS
        '''
        self._packet = packet
        record = None
        raw_packet = packet
        ethernet_frame = Ethernet(raw_packet)
        ethernet_data = ethernet_frame.data
        udp_packet = ethernet_data.data
        print(ethernet_frame.__dict__)
        if ('arp' in ethernet_frame.__dict__):
            record = self.extract_arp(packet, timestamp, interface_name)
        else:
            dst_mac = hexlify(ethernet_frame['dst']).decode('ascii')
            if (udp_packet['sport']==138):
                if dst_mac == 'ffffffffffff':
                    record = self.extract_nbds(packet, timestamp, interface_name)
        return record
