'''
    PBASingleton class

    This is an abstract class for simpler implementations of the
    Singleton Pattern.

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"


class PBASingleton:
    '''
        PBASingleton
        
        Represents a simple and elegant abstraction of the Singleton Pattern
    '''

    def __new__(cls, *args, **kwargs):
        '''
            It is a static method called when is created a new instance of class
            cls. Other arguments are passed to the constructor of class cls.

            Normally such method returns a new instance of class cls.

            In order to implement the Singleton Pattern such method is weaved
            and through an hack, about the presence of variable __instance,
	    it acquires knowledge about the existence of an instance of class
            cls. When the variable __instance is not a variable of class cls
            it is created through normal invocation of method __new.

            On a successive invocation variable __instance exists and 
            is realized the principle of the Singleton Pattern.
        '''
        if '__instance' not in vars(cls):
            cls.__instance = cls.__new__(cls, *args, **kwargs)
        return cls.__instance
