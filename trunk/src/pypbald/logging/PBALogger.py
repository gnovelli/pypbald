'''
    PBALogger class

    Main responsibility:
    - rotating logfiles of single filtered broadcast packets for forensics and
      debugging

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"

import logging
import logging.handlers
from pypbald.PBASingleton import PBASingleton


class PBALogger(PBASingleton):
    '''
        PBALogger
        
        It is a wrapper of standard python logging module

        It is implemented as a Singleton Pattern
    '''
    _pba = None
    _text = None
    my_logger = None
    handler = None
    LOG_FILENAME = None

    def __init__(self, pba):
        '''
            PBALogger constructor

            Initializes logging module and files
        '''
        import os
        self._pba = pba
        self.LOG_FILENAME = self._pba.cfg('log_filename');
        
        # Ensure the log directory exists
        log_dir = os.path.dirname(self.LOG_FILENAME)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Set up a specific logger with our desired output level
        self.my_logger = logging.getLogger('MyLogger')
        self.my_logger.setLevel(logging.DEBUG)

        # Add the log message handler to the logger
        self.handler = logging.handlers.RotatingFileHandler(
                      self.LOG_FILENAME, maxBytes=1048576, backupCount=64)

        self.my_logger.addHandler(self.handler)

    def log(self, Text):
        '''
            Text logging

            Text contents must be well formatted by caller
        '''
        self._text = Text
        #self.my_logger.debug(Text)
        result = 0
        return result
