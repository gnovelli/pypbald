'''
    PBARecordNBDS

    A representation of broadcast packets of type NBDS

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"

from binascii import hexlify
from datetime import datetime
from pypbald.records.PBARecord import PBARecord

class PBARecordNBDS(PBARecord):
    '''
        PBARecordNBDS

        A representation of broadcast packets of type NBDS

        Stores the following informations:
        - packet timestamp
        - source MAC address
        - source IP address
        - destionation IP address
        - decoded source netbios name
        - encoded source netbios name
        - decoded destination netbios name
        - encoded destination netbios name
    '''
    _thetime = None
    _src_mac = None
    _src_ip = None
    _dst_ip = None
    _src_netbios_name = None
    _src_netbios_name_hex = None
    _src_netbios_name_encoded =  None
    _dst_netbios_name = None
    _dst_netbios_name_hex = None
    _dst_netbios_name_encoded = None

    def assign(
                self,
                thetime,
                src_mac,
                src_ip,
                dst_ip,
                src_netbios_name,
                src_netbios_name_hex,
                src_netbios_name_encoded,
                dst_netbios_name,
                dst_netbios_name_hex,
                dst_netbios_name_encoded):
        '''
            Initializes class fields

            Stores the following informations:
            - packet timestamp
            - source MAC address
            - source IP address
            - destionation IP address
            - decoded source netbios name
            - encoded source netbios name
            - decoded destination netbios name
            - encoded destination netbios name
        '''
        self._thetime = thetime
        self._src_mac = src_mac
        self._src_ip = src_ip
        self._dst_ip = dst_ip
        self._src_netbios_name = src_netbios_name
        self._src_netbios_name_hex = src_netbios_name_hex
        self._src_netbios_name_encoded =  src_netbios_name_encoded
        self._dst_netbios_name = dst_netbios_name
        self._dst_netbios_name_hex = dst_netbios_name_hex
        self._dst_netbios_name_encoded = dst_netbios_name_encoded

    def gettext(self):
        '''
            Prepares text content for logging
        '''
        text = '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"' % (
            self._thetime,
            self._src_mac,
            self._src_ip,
            self._dst_ip,
            self._src_netbios_name,
            self._src_netbios_name_hex,
            self._src_netbios_name_encoded,
            self._dst_netbios_name,
            self._dst_netbios_name_hex,
            self._dst_netbios_name_encoded)
        return text
    
    def update(self, backend):
        '''
            Updates backend when needed

            In order to make such update:
            - extract date and time according to format %Y%m%d%H%M%S
            - compute current record hash
            - if such hash is in the dictionary
            -- updates count (count) and last timestamp of packet (last_seen)
               in table pba_nbds_summary
            - otherwise insert the new record in the database and the dictionary
        '''
        last_seen = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_value = backend.make_hash_nbds(self._src_mac,
                                     self._src_ip,
                                     self._dst_ip,
                                     self._src_netbios_name_encoded,
                                     self._dst_netbios_name_encoded
                                    )
        if backend.getsummarynbds().has_key(hash_value):
            backend.execute("""
                   UPDATE pba_nbds_summary
                   SET count = count +1, last_seen = """ + last_seen + """
                   WHERE src_mac = '""" + self._src_mac + """' 
                         AND
                         src_ip = '""" + self._src_ip + """'
                         AND
                         dst_ip = '""" + self._dst_ip + """'
                         AND
                         src_netbios_name_encoded = '""" +
                         self._src_netbios_name_encoded + """'
                         AND
                         dst_netbios_name_encoded = '""" +
                         self._dst_netbios_name_encoded + """'""")
        else:
            backend.execute("""
                   INSERT INTO pba_nbds_summary (
                    src_mac,
                    src_ip,
                    dst_ip,
                    src_netbios_name,
                    src_netbios_name_encoded,
                    dst_netbios_name,
                    dst_netbios_name_encoded,
                    first_seen)
                   VALUES
                    (
                        '"""+self._src_mac+"""',
                        '"""+self._src_ip+"""',
                        '"""+self._dst_ip+"""',
                        '"""+self._src_netbios_name+"""',
                        '"""+self._src_netbios_name_encoded+"""',
                        '"""+self._dst_netbios_name+"""',
                        '"""+self._dst_netbios_name_encoded+"""',
                        """+last_seen+""")
                    """)
                     
        stmt = """  select DISTINCT
                        src_mac,
                        src_ip,
                        dst_ip,
                        src_netbios_name_encoded,
                        dst_netbios_name_encoded
                    from
                        pba_nbds_summary
                    WHERE
                        src_mac = '""" + self._src_mac + """'
                    AND
                        src_ip = '""" + self._src_ip + """'
                    AND
                        dst_ip = '""" + self._dst_ip + """'
                    AND
                        src_netbios_name_encoded =
                        '""" + self._src_netbios_name_encoded + """'
                    AND
                        dst_netbios_name_encoded =
                        '""" + self._dst_netbios_name_encoded + """'"""
        rows = backend.query(backend._localdb_conn, stmt)
        for row in rows:
            hash_value = backend.make_hash_nbds(row['src_mac'],
                                       row['src_ip'],
                                       row['dst_ip'],
                                       row['src_netbios_name_encoded'],
                                       row['dst_netbios_name_encoded']
                                    )
            backend.getsummarynbds()[hash_value] = row

    def isaname(self):
        return self._dst_netbios_name_encoded.find(
            'ABACFPFPENFDECFCEPFHFDEFFPFPAC')==-1

    def insert(self, backend):
        '''
            Stores itself on detail table pba_nbds
            Such choice is based on boolean flag detail from pypbald.config

            Furthermore inserts raw packet in detail table pba_nbds_raw
            Such choice is based on boolean flag raw from pypbald.config
        '''
        hash_value = backend.make_hash_nbds(
							self._src_mac,
							self._src_ip,
							self._dst_ip,
							self._src_netbios_name_encoded,
							self._dst_netbios_name_encoded)

        stmt = """
                   INSERT INTO pba_nbds (hash,
                                         thetime,
                                         src_mac,
                                         src_ip,
                                         dst_ip,
                                         src_netbios_name,
                                         src_netbios_name_hex,
                                         src_netbios_name_encoded,
                                         dst_netbios_name,
                                         dst_netbios_name_hex,
                                         dst_netbios_name_encoded)
                   VALUES
                     ('"""+hash_value+"""',
                      '"""+self._thetime+"""',
                      '"""+self._src_mac+"""',
                      '"""+self._src_ip+"""',
                      '"""+self._dst_ip+"""',
                      '"""+self._src_netbios_name+"""',
                      '"""+self._src_netbios_name_hex+"""',
                      '"""+self._src_netbios_name_encoded+"""',
                      '"""+self._dst_netbios_name+"""',
                      '"""+self._dst_netbios_name_hex+"""',
                      '"""+self._dst_netbios_name_encoded+"""')
                     """
        if (backend.getpba().cfg('localdb_detail')):
            backend.execute_local(stmt)
        if (backend.getpba().cfg('remotedb_detail')):
            backend.execute_remote(stmt)

        raw = hexlify(self._pkt)
        stmt = """
                   INSERT INTO pba_nbds_raw (hash,raw)
                   VALUES
                     ('"""+hash_value+"""',
                      '"""+raw+"""')
                     """
        if (backend.getpba().cfg('localdb_raw')):
            backend.execute_local(stmt)
        if (backend.getpba().cfg('remotedb_raw')):
            backend.execute_remote(stmt)
