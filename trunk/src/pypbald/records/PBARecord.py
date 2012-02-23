'''
    PBARecord class

    A raw abstraction of filtered broadcast packets

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"

class PBARecord:
    '''
        PBARecord
        
        It's an abstract class for all filtered broadcast packets
        
        It's for memoization of packet and its timestamp in their original form
        as captured through library pcap
    '''
    _pkt = None
    _ts = None
    def __init__(self, packet, timestamp):
        '''
            PBARecord constructor
        '''
        self._pkt = packet
        self._ts = timestamp