'''  
    PBABackend class
    
    Its main responsibilities are:
    - insertion and updated of captured records on databases
    - empty databases tables when debugging is enabled
    
    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"

from binascii import hexlify
import hashlib
import mysql.connector
from mysql.connector import Error
from pypbald.PBASingleton import PBASingleton

class PBABackend(PBASingleton):
    '''
        PBABackend
        
        This class gives access to two databases:
        - local database
        - remote database
        
        The choice to rely upon two databases is aimed at:
        - obtaining a real time backup of information
        - give access to other applications, even remote ones, to such data

        This class is implemented as a Singleton Pattern
    '''

    _localdb_conn = None
    _remotedb_conn = None
    _localdb_cursor = None
    _remotedb_cursor = None
    _pba = None
    _summary_nbds = None

    def __init__(self,pba):
        '''
            PBABackend constructor

            It creates connections to local and remote databases according to
            configuration choices read from pypbald.config.

            While establishing such connections it relies upon DictCursor
            cursors to keep access to both rows and columns for a simple
            query reflection pattern.

            When debugging is enabled database tables are reset through 
            SQL TRUNCATE statements.

            Furthermore, it initializes a dictionary containing a summary
            of filtered broadcast packets.

            It shows a method to close databases connections according to
            configuration choices read from pypbald.config.
        '''
        self._pba = pba
        if (self._pba.cfg('localdb_enabled')):
            self._localdb_conn = mysql.connector.connect(
                host = self._pba.cfg('localdb_hostname'),
                user = self._pba.cfg('localdb_username'),
                password = self._pba.cfg('localdb_password'),
                database = self._pba.cfg('localdb_database'))

        if (self._pba.cfg('remotedb_enabled')):
            self._remotedb_conn = mysql.connector.connect(
                host = self._pba.cfg('remotedb_hostname'),
                user = self._pba.cfg('remotedb_username'),
                password = self._pba.cfg('remotedb_password'),
                database = self._pba.cfg('remotedb_database'))
        if (self._pba.cfg('debug')):
            self.reset()
        self.summary_nbds()
        self.summary_arp()

    def reset(self):
        '''
            Tables reset
        '''
        self.execute_local('TRUNCATE TABLE pba_nbds')
        self.execute_local('TRUNCATE TABLE pba_nbds_summary')
        self.execute_local('TRUNCATE TABLE pba_nbds_raw')
        self.execute_local('TRUNCATE TABLE pba_arp')
        self.execute_local('TRUNCATE TABLE pba_arp_summary')
        self.execute_local('TRUNCATE TABLE pba_arp_raw')
        
        self.execute_remote('TRUNCATE TABLE pba_nbds')
        self.execute_remote('TRUNCATE TABLE pba_nbds_summary')
        self.execute_remote('TRUNCATE TABLE pba_nbds_raw')
        self.execute_remote('TRUNCATE TABLE pba_arp')
        self.execute_remote('TRUNCATE TABLE pba_arp_summary')
        self.execute_remote('TRUNCATE TABLE pba_arp_raw')

    def execute(self, conn, stmt):
        '''
            Database connection
        '''
        cursor = conn.cursor(dictionary=True)
        cursor.execute (stmt)
        cursor.close()
        conn.commit()

    def execute_local(self, stmt):
        '''
            Connection to local database according to
            configuration choices read from pypbald.config.
        '''
        if (self._pba.cfg('localdb_enabled')):
            conn = self._localdb_conn
            cursor = conn.cursor(dictionary=True)
            cursor.execute (stmt)
            cursor.close()
            conn.commit()

    def execute_remote(self, stmt):
        '''
            Connection to remote database according to
            configuration choices read from pypbald.config.
        '''
        if (self._pba.cfg('remotedb_enabled')):
            conn = self._remotedb_conn
            cursor = conn.cursor(dictionary=True)
            cursor.execute (stmt)
            cursor.close()
            conn.commit()

    def execute(self,stmt):
        '''
            Execution of SQL statements on databases according to
            configuration choices read from pypbald.config.
        '''
        self.execute_local(stmt)
        self.execute_remote(stmt)

    def query(self, conn, stmt):
        '''
            Execution of SQL query on a database

            Returns fetched rows
        '''
        cursor = conn.cursor(dictionary=True)
        cursor.execute (stmt)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def summary_nbds(self):
        '''
            Initializes NBDS summary dictionary
        '''
        tempdict = {}
        if self._localdb_conn is not None:
            stmt = "select * from pba_nbds_summary"
            rows = self.query(self._localdb_conn, stmt)
            for row in rows:
                hash_value = self.make_hash_nbds(
                    row['src_mac'],
                    row['src_ip'],
                    row['dst_ip'],
                    row['src_netbios_name_encoded'],
                    row['dst_netbios_name_encoded'])
                if hash_value not in tempdict:
                    tempdict[hash_value]=row
                if (self._pba.cfg('debug')):
                    print(hash_value, row)
        self._summary_nbds = tempdict
        self._pba._summary_nbds = self._summary_nbds
        return tempdict

    def summary_arp(self):
        '''
            Initializes ARP summary dictionary

        '''
        tempdict = {}
        if self._localdb_conn is not None:
            stmt = "select * from pba_arp_summary"
            rows = self.query(self._localdb_conn, stmt)
            for row in rows:
                hash_value = self.make_hash_arp(
                    row['src_mac'],
                    row['src_ip'])
                if hash_value not in tempdict:
                    tempdict[hash_value]=row
                if (self._pba.cfg('debug')):
                    print(hash_value, row)
        self._summary_arp = tempdict
        self._pba._summary_arp = self._summary_arp
        return tempdict

    def close(self):
        '''
            Closes databases connections
        '''
        if (self._pba.cfg('localdb_enabled')):
            self._localdb_conn.close ()
            self._localdb_conn = None
            self._localdb_cursor = None
        if (self._pba.cfg('remotedb_enabled')):
            self._remotedb_conn.close ()
            self._remotedb_conn = None
            self._remotedb_cursor = None

    def make_hash_nbds(self,
             src_mac,
             src_ip,
             dst_ip,
             src_netbios_name_encoded,
             dst_netbios_name_encoded):
        '''
            Hash encoding of each item of NBDS summary

            It is used to have unique dictionary keys

            Hash is computed on a string concatenation of:
            - source MAC address
            - source IP address
            - destination netmask
            - binary encoding of source netbios name
            - binary encoding of destionation netbios name

            An MD5 digest is returned from such computation

            Returns an hexadecimal encoding of such a digest
        '''
        str = ""
        str = str + src_mac
        str = str + src_ip
        str = str + dst_ip
        str = str + src_netbios_name_encoded
        str = str + dst_netbios_name_encoded
        hash = hashlib.md5()
        hash.update(str.encode('utf-8'))
        hash_value = hexlify(hash.digest()).decode('ascii')
        return hash_value

    def make_hash_arp(self,
             src_mac,
             src_ip):
        '''
            Hash encoding of each item of ARP summary

            It is used to have unique dictionary keys

            Hash is computed on a string concatenation of:
            - source MAC address
            - source IP address

            An MD5 digest is returned from such computation

            Returns an hexadecimal encoding of such a digest
        '''
        str = ""
        # Handle bytes objects from hexlify() in Python 3
        if isinstance(src_mac, bytes):
            src_mac = src_mac.decode('utf-8')
        if isinstance(src_ip, bytes):
            src_ip = src_ip.decode('utf-8')
        str = str + src_mac
        str = str + src_ip
        hash = hashlib.md5()
        hash.update(str.encode('utf-8'))
        hash_value = hexlify(hash.digest()).decode('ascii')
        return hash_value

    def getpba(self):
        return self._pba

    def getsummarynbds(self):
        return self._summary_nbds

    def getsummaryarp(self):
        return self._summary_arp