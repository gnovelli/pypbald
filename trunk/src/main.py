'''  
    Execution module.

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"


from PBA import PBA

def main():
    '''
        Entry point.
    '''
    pba = PBA()
    pba.startup()
    pba.listen()
    pba.shutdown()

if __name__ == '__main__':
    main()
