'''
    PBARecordARPRequest class

    A representation of broadcast packets of type ARP request

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"

from binascii import hexlify
from datetime import datetime
from pypbald.records.PBARecord import PBARecord

class PBARecordARPRequest(PBARecord):
    '''
        PBARecordARPRequest

        A representation of broadcast packets of type ARP request

        Stores the following informations:
        - packet timestamp 
        - source MAC address 
        - source IP address 
    '''
    _thetime = None
    _src_mac = None
    _src_ip = None

    def assign(
                self,
                thetime,
                src_mac,
                src_ip):
        '''
            Initializes class fields

            Stores the following informations:
            - packet timestamp
            - source MAC address
            - source IP address
        '''
        self._thetime = thetime
        self._src_mac = src_mac
        self._src_ip = src_ip

    def gettext(self):
        '''
            Prepares text content for logging
        '''
        text = '"%s","%s","%s"' % (
            self._thetime,
            self._src_mac,
            self._src_ip)
        return text
    
    def update(self, backend):
        '''
            Updates backend when needed

            In order to make such update:
            - extract date and time according to format %Y%m%d%H%M%S
            - compute current record hash
            - if such hash is in the dictionary
            -- updates count (count) and last timestamp of packet (last_seen)
               in table pba_arp_summary
            - otherwise insert the new record in the database and the dictionary
        '''
        last_seen = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_value = backend.make_hash_arp(self._src_mac,
                                     self._src_ip)
        if hash_value in backend.getsummaryarp():
            backend.execute("""
                   UPDATE pba_arp_summary
                   SET count = count +1, last_seen = """ + last_seen + """
                   WHERE src_mac = '""" + self._src_mac + """' 
                         AND
                         src_ip = '""" + self._src_ip + """'""")
        else:
            backend.execute("""
                   INSERT INTO pba_arp_summary (
                    src_mac,
                    src_ip,
                    first_seen)
                   VALUES
                    (
                        '"""+self._src_mac+"""',
                        '"""+self._src_ip+"""',
                        """+last_seen+""")
                    """)
                     
        stmt = """  select DISTINCT
                        src_mac,
                        src_ip
                    from
                        pba_arp_summary
                    WHERE
                        src_mac = '""" + self._src_mac + """'
                    AND
                        src_ip = '""" + self._src_ip + """'"""

        rows = backend.query(backend._localdb_conn, stmt)
        for row in rows:
            hash_value = backend.make_hash_arp(row['src_mac'],
                                       row['src_ip']
                                    )
            backend.getsummaryarp()[hash_value] = row

    def insert(self, backend):
        '''
            Stores itself on detail table pba_arp
            Such choice is based on boolean flag detail from pypbald.config

            Furthermore inserts raw packet in detail table pba_arp_raw
            Such choice is based on boolean flag raw from pypbald.config
        '''
        hash_value = backend.make_hash_arp(
                                            self._src_mac,
                                            self._src_ip,
                                            )

        stmt = """
                   INSERT INTO pba_arp (hash,
                                         thetime,
                                         src_mac,
                                         src_ip)
                   VALUES
                     ('"""+hash_value+"""',
                      '"""+self._thetime+"""',
                      '"""+self._src_mac+"""',
                      '"""+self._src_ip+"""')
                     """
        if (backend.getpba().cfg('localdb_detail')):
            backend.execute_local(stmt)
        if (backend.getpba().cfg('remotedb_detail')):
            backend.execute_remote(stmt)

        raw = hexlify(self._pkt)
        stmt = """
                   INSERT INTO pba_arp_raw (hash,raw)
                   VALUES
                     ('"""+hash_value+"""',
                      '"""+raw+"""')
                     """
        if (backend.getpba().cfg('localdb_raw')):
            backend.execute_local(stmt)
        if (backend.getpba().cfg('remotedb_raw')):
            backend.execute_remote(stmt)
