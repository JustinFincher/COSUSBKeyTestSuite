import os
import hashlib
from Controller.Singleton import *
from Data.APDU import *
from Controller.DeviceManager import *
from Controller.LogManager import LogManager
from Data.StatCode import *
from enum import Enum
from Controller.LogManager import *
from datetime import datetime, timedelta
from Data.Test import *
import time


class FileLocationType(Enum):
    MF = 0
    ADF = 1
    GPKF = 2
    IKF = 3
    EFTokenInfo = 4
    EFPublic = 5
    EFPrivate = 6

class Helper(object,metaclass=Singleton):



    def getFID(self,locationType):
        if locationType == FileLocationType.MF:
            return "3F00"
        if locationType == FileLocationType.ADF:
            return "2001"
        if locationType == FileLocationType.GPKF:
            return "FFFD"
        if locationType == FileLocationType.IKF:
            return "FFFE"
        if locationType == FileLocationType.EFTokenInfo:
            return "A001"
        if locationType == FileLocationType.EFPublic:
            return "A002"
        if locationType == FileLocationType.EFPrivate:
            return "A003"


    def getMd5HashHex(self,inputStr):
        print("getMd5HashHex")
        print(inputStr)
        print(inputStr.encode())
        print(inputStr.encode('utf-8'))


        hexStr = hashlib.md5(inputStr.encode('utf-8')).hexdigest()
        print(hexStr)
        return str(hexStr)

    def getChallengeMsg(self):
        LogManager().addLogStr("Getting Challenge")
        apdu = APDU({"CLA":"00",
                     "INS":"84",
                     "P1":"00",
                     "P2":"00",
                     "Lc":None,
                     "Data":None,
                     "Le":"08"})
        dict = DeviceManager().sendAPDU(apdu)
        print("getChallengeMsg Dict =")
        print(dict)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode == StatCodeType.STAT_CODE_SUCCESS:
                return dict["msg"]

        return None

    def getSelectFileDict(self,pos):
        LogManager().addLogStr("Selecting File For Pos:" + str(pos))
        print("Selecting File with Pos" + str(pos))
        apdu = APDU({"CLA": "00",
                     "INS": "A4",
                     "P1": "00",
                     "P2": "00",
                     "Lc": "02",
                     "Data": self.getFID(pos),
                     "Le": None})
        dict = DeviceManager().sendAPDU(apdu)
        return dict


    def getVerifyPinDict(self,data,KID = "00"):
        apdu = APDU({"CLA": "00",
                     "INS": "82",
                     "P1": "00",
                     "P2": KID,
                     "Lc": "08",
                     "Data": data,
                     "Le": None})

        print("getVerifyPinDict apdu = " + apdu.stringRepresentation())
        dict = DeviceManager().sendAPDU(apdu)
        print("getVerifyPinDict Dict = " + str(dict))
        return dict

    def getSelectPKIADFDict(self):
        mfDict = self.getSelectFileDict(FileLocationType.MF)
        if (mfDict != None) and ('statCode' in mfDict):
            statCode = mfDict["statCode"].statCode
            if statCode == StatCodeType.STAT_CODE_SUCCESS:
                adfDict = self.getSelectFileDict(FileLocationType.ADF)
                return adfDict
        return None

    def getPubKeyDict(self,KID = "00"):
        LogManager().addLogStr("Getting Public Key Dict For KID = " + str(KID))
        apdu = APDU({"CLA": "80",
                     "INS": "E6",
                     "P1": "2A",
                     "P2": KID,
                     "Lc": None,
                     "Data": None,
                     "Le": "FF"})

        print("getPubKeyDict apdu = " + apdu.stringRepresentation())
        dict = DeviceManager().sendAPDU(apdu)
        print("getPubKeyDict Dict = " + str(dict))
        return dict

    def getMSESignDict(self, KID):
        raise NotImplementedError("Too LAZY to do this")
        pass

    def getMSEGenParDict(self,KID = "00",usage = "22", additionLength = 4):
        apdu = APDU({"CLA": "00",
                     "INS": "22",
                     "P1": "01",
                     "P2": "B8",
                     "Lc": '{:02X}'.format(4 + additionLength),
                     "Data": "8302" + KID + usage,
                     "Le": None})

        print("getPubKeyDict apdu = " + apdu.stringRepresentation())
        dict = DeviceManager().sendAPDU(apdu)
        print("getPubKeyDict Dict = " + str(dict))
        return dict

    def getBinaryReadDict(self,p1,p2,length = "08"):
        apdu = APDU({"CLA": "00",
                     "INS": "B0",
                     "P1": p1,
                     "P2": p2,
                     "Lc": None,
                     "Data": None,
                     "Le": length})
        print("getBinaryReadDict apdu = " + apdu.stringRepresentation())
        dict = DeviceManager().sendAPDU(apdu)
        print("getBinaryReadDict Dict = " + str(dict))
        return dict

    pass

    def getBinaryWriteDict(self,p1,p2,data):
        apdu = APDU({"CLA": "00",
                     "INS": "D6",
                     "P1": p1,
                     "P2": p2,
                     "Lc": '{:02X}'.format(len(data)),
                     "Data": data,
                     "Le": None})
        print("getBinaryReadDict apdu = " + apdu.stringRepresentation())
        dict = DeviceManager().sendAPDU(apdu)
        print("getBinaryReadDict Dict = " + str(dict))
        return dict
    pass

    def getGenKeyPairDict(self):
        apdu = APDU({"CLA": "00",
                     "INS": "46",
                     "P1": "00",
                     "P2": "00",
                     "Lc": "02",
                     "Data": "0400",
                     "Le": None})
        print("getGenKeyPairDict apdu = " + apdu.stringRepresentation())
        dict = DeviceManager().sendAPDU(apdu)
        print("getGenKeyPairDict Dict = " + str(dict))
        return dict

    def replaceFFWithFE(self,x):
        chunks, chunk_size = len(x), 2
        listOfHex =  [ x[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
        listOfReplacedHex = []
        for h in listOfHex:
            listOfReplacedHex.append(h.upper().replace("FF", "FE"))

        res = ''.join(listOfReplacedHex)
        return res

    pass
