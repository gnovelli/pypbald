'''
    PBASniffer class

    A simple wrapper to pcap library for passive listening of
    filtered broadcast packets:
    - initializes pcap with a filter
    - captures packets (through pcap)
    - gives packets to parser (PBAParser)
    - receives a record (a subclass of abstract PBARecord class)
    - logs record as text (PBALogger)
    - inserts or update the record on databases (PBABackend)

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"

import pcap
from pypbald.PBASingleton import PBASingleton
from pypbald.records.PBARecordNBDS import PBARecordNBDS
from pypbald.records.PBARecordARPRequest import PBARecordARPRequest

class PBASniffer(PBASingleton):
    '''
        PBASniffer
        
        A simple wrapper to pcap library for passive listening of
        filtered broadcast packets:
        - initializes pcap with a filter
        - captures packets (through pcap)
        - gives packets to parser (PBAParser)
        - receives a record (a subclass of abstract PBARecord class)
        - logs record as text (PBALogger)
        - inserts or update the record on databases (PBABackend)

        This class is implemented as a Singleton Pattern
    '''
    _pba = None
    _pc = None

    def __init__(self, pba):
        '''
            PBASniffer constructor

            Initializes pcap filter according to pypbald configuration
        '''
        self._pba = pba
        name = "eth0"
        self._pc = pcap.pcap(name)
        self._pc.setfilter(self._pba.cfg('filter'))

    def listen(self, backend, logger, parser):
        '''
            Listening loop

            Allows raw console debugging according to pypbald configuration

            When NBDS destination is NOT __MSBROWSE__ backend is updated

            CTRL+C is needed to stop listening
        '''
        try:
            print 'listening on %s: %s' % (self._pc.name, self._pc.filter)
            for timestamp, packet in self._pc:
                record = parser.parse(packet, timestamp)
                if isinstance(record,PBARecordNBDS):
                    text = record.gettext()
                    if (self._pba.cfg('debug')):
                        print text
                    logger.log(text)
                    if record.isaname():
                        record.insert(backend)
                        record.update(backend)
                if isinstance(record,PBARecordARPRequest):
                    text = record.gettext()
                    if (self._pba.cfg('debug')):
                        print text
                    logger.log(text)
                    record.insert(backend)
                    record.update(backend)

        except KeyboardInterrupt:
            nrecv, ndrop, nifdrop = self._pc.stats()
            print '\n%d received packets' % nrecv
            print '%d kernel dropped packets' % ndrop
            print '%d nifdrop' % nifdrop
