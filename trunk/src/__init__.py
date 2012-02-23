''' 
    A passive analyzer of broadcast packets, aimed at discovery of unknown hosts
    in a LAN.

    This software allows to discover hosts in a LAN and to know:
    - their ip address
    - their mac address
    - their smb group/domain

    This knowledge is obtained through passive listening of two types of
    broadcast packets:
    - ARP
    - UDP with source port 138
 
    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"



