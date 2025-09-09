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
import netifaces
import threading
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
    _sniffers = {}
    _threads = []

    def __init__(self, pba):
        '''
            PBASniffer constructor

            Initializes pcap filters for all available network interfaces
        '''
        self._pba = pba
        self._sniffers = {}
        self._threads = []
        
        # Get all network interfaces
        interfaces = netifaces.interfaces()
        print(f"Available interfaces: {interfaces}")
        
        for iface in interfaces:
            # Skip loopback interface
            if iface == 'lo':
                continue
                
            try:
                # Initialize pcap for this interface
                sniffer = pcap.pcap(iface)
                sniffer.setfilter(self._pba.cfg('filter'))
                self._sniffers[iface] = sniffer
                print(f"Initialized sniffer for interface: {iface}")
            except Exception as e:
                print(f"Warning: Could not initialize sniffing on {iface}: {e}")
        
        if not self._sniffers:
            print("Warning: No network interfaces available for sniffing")

    def _sniff_interface(self, iface, sniffer, backend, logger, parser):
        '''
            Sniffing function for a single interface (runs in separate thread)
        '''
        try:
            print(f'listening on {iface}: {sniffer.filter}')
            for timestamp, packet in sniffer:
                record = parser.parse(packet, timestamp, iface)
                if isinstance(record, PBARecordNBDS):
                    text = f"[{iface}] {record.gettext()}"
                    if self._pba.cfg('debug'):
                        print(text)
                    logger.log(text)
                    if record.isaname():
                        record.insert(backend)
                        record.update(backend)
                if isinstance(record, PBARecordARPRequest):
                    text = f"[{iface}] {record.gettext()}"
                    if self._pba.cfg('debug'):
                        print(text)
                    logger.log(text)
                    record.insert(backend)
                    record.update(backend)
                    
        except KeyboardInterrupt:
            pass  # Handle graceful shutdown
        except Exception as e:
            print(f"Error on interface {iface}: {e}")
        finally:
            try:
                nrecv, ndrop, nifdrop = sniffer.stats()
                print(f'\nInterface {iface} statistics:')
                print(f'  {nrecv} received packets')
                print(f'  {ndrop} kernel dropped packets') 
                print(f'  {nifdrop} interface dropped packets')
            except:
                print(f'Could not retrieve statistics for {iface}')

    def listen(self, backend, logger, parser):
        '''
            Multi-interface listening loop

            Starts a separate thread for each network interface.
            
            CTRL+C is needed to stop listening
        '''
        if not self._sniffers:
            print("No interfaces available for sniffing")
            return
            
        print(f"Starting sniffing on {len(self._sniffers)} interfaces...")
        
        # Start a thread for each interface
        for iface, sniffer in self._sniffers.items():
            thread = threading.Thread(
                target=self._sniff_interface,
                args=(iface, sniffer, backend, logger, parser),
                name=f"sniffer-{iface}"
            )
            thread.daemon = True
            thread.start()
            self._threads.append(thread)
        
        try:
            # Wait for all threads to complete
            for thread in self._threads:
                thread.join()
        except KeyboardInterrupt:
            print("\nShutdown requested, stopping all sniffers...")
            # Threads will naturally terminate when main thread exits
