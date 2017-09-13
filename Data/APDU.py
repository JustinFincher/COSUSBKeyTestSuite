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
        try:
            self.CLA = dict["CLA"] if ('CLA' in dict and dict["CLA"]!=None) else ''
            self.INS = dict["INS"] if ('INS' in dict and dict["INS"]!=None) else ''
            self.P1 =  dict["P1"] if ('P1' in dict and dict["P1"]!=None) else ''
            self.P2 = dict["P2"] if ('P2' in dict and dict["P2"]!=None) else ''
            self.Lc =  dict["Lc"] if ('Lc' in dict and dict["Lc"]!=None) else ''
            self.Data = dict["Data"] if ('Data' in dict and dict["Data"]!=None) else ''
            self.Le =  dict["Le"] if ('Le' in dict and dict["Le"]!=None) else ''
        except:
            pass
    pass


    def byteRepresentation(self):
        return bytes.fromhex(self.stringRepresentation())

    def stringRepresentation(self):
        stringRep = '{}{}{}{}{}{}{}'.format(self.CLA, self.INS,self.P1,self.P2,self.Lc,self.Data,self.Le)
        print(stringRep)
        return stringRep

    def getHexLength(self):
        return len(self.byteRepresentation())