'''
    PBA class

    Singleton class whose main responsibily is to read and store pypald
    configuration.

    This class has the following responsibilities too:
    - initialize other classes instances
    - realize listening loop 
    - deinitialize other classes instances

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"

import configparser
from pypbald.PBASingleton import PBASingleton
from pypbald.backend.PBABackend import PBABackend
from pypbald.logging.PBALogger import PBALogger
from pypbald.parsing.PBAParser import PBAParser
from pypbald.sniffing.PBASniffer import PBASniffer


class PBA(PBASingleton):
    '''
         PBA
        
         Implemented according to Singleton Pattern inherited from PBASingleton
         superclass.

         It shows the following methods:
         - read_config which reads pypbald configuration
         - startup which initializes other classes
         - listen which realizes listening loop
         - shutdown which closes databases and destroys other classes instances
    '''

    _cfg = None
    _backend = None
    _logger = None
    _parser = None
    _sniffer = None
    _summary_nbds = None
    _summary_arp = None

    def __init__(self):
        '''
            Calls method read_config which reads pypbald configuration 
	    and stores it in _cfg dictionary.
        '''
        self.read_config()

    def read_config(self):
        '''
            Reads pypbald configuration and stores it in _cfg dictionary.
        '''
        self._cfg = {'Application': 'pypbald'}

        config = configparser.RawConfigParser()
        config.read('../pypbald.config')

        self._cfg['debug'] = config.getboolean('global','debug')
        self._cfg['filter'] = config.get('global','filter')
        self._cfg['log_filename'] = config.get('global','log_filename')

        self._cfg['localdb_enabled'] = config.getboolean('localdb', 'enabled', fallback=True)
        self._cfg['localdb_username'] = config.get('localdb','username')
        self._cfg['localdb_password'] = config.get('localdb','password')
        self._cfg['localdb_database'] = config.get('localdb','database')
        self._cfg['localdb_detail'] = config.getboolean('localdb','detail')
        self._cfg['localdb_raw'] = config.getboolean('localdb','raw')

        self._cfg['remotedb_enabled'] = config.getboolean('remotedb','enabled')
        self._cfg['remotedb_hostname'] = config.get('remotedb','hostname')
        self._cfg['remotedb_username'] = config.get('remotedb','username')
        self._cfg['remotedb_password'] = config.get('remotedb','password')
        self._cfg['remotedb_database'] = config.get('remotedb','database')
        self._cfg['remotedb_detail'] = config.getboolean('remotedb','detail')
        self._cfg['remotedb_raw'] = config.getboolean('remotedb','raw')

    def startup(self):
        '''
            Initializes other classes.

            Such classes are:
            - PBABackend which instance is memoized in _backend
            - PBALogger which instance is memoized in _logger
            - PBAParser which instance is memoized in _parser
            - PBASniffer which instance is memoized in _sniffer
        '''
        self._backend = PBABackend(self)
        self._logger = PBALogger(self)
        self._parser = PBAParser(self)
        self._sniffer = PBASniffer(self)


    def listen(self):
        '''
            Starts listening loop of _sniffer instance of the class PBASniffer.
        '''
        self._sniffer.listen(self._backend, self._logger, self._parser)

    def shutdown(self):
        '''
            Destroys other classes instances.

            Closes backend and related databases used to store information
	    extracted from filtered broadcast packets.
        '''
        self._backend.close()
        self._backend = None
        self._logger = None
        self._parser = None
        self._sniffer = None


    def summary_nbds(self):
        '''
            Returns a dictionary which keeps in memory all NBDS informations
	    stored in databases for faster access to them.
        '''
        return self._summary_nbds

    def summary_arp(self):
        '''
            Returns a dictionary which keeps in memory all ARP informations
	    stored in databases for faster access to them.
        '''
        return self._summary_arp

    def cfg(self, key):
        '''
            Gives a dictionary access to pypbald configuration.
        '''
        return self._cfg[key]

