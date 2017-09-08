import os

class APDU(object):

    CLA = ''
    INS = ''
    P1 = ''
    P2 = ''
    Lc = ''
    Data = ''
    Le = ''

    def __init__(self, dict = dict):
        pass


    def byteRepresentation(self):
        return bytes.fromhex(self.stringRepresentation())

    def stringRepresentation(self):
        return self.CLA+self.INS+self.P1+self.P2

    def getLength(self):
        return 0