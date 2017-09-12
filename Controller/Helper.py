import os
import hashlib
from Controller.Singleton import *
from Data.APDU import *
from Controller.DeviceManager import *
from Controller.LogManager import *
from Data.StatCode import *
from enum import Enum
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
        return hashlib.md5(inputStr).hexdigest()

    def getChallengeMsg(self):
        LogManager().addLog("Geting Challenge")
        apdu = APDU({"CLA":"00",
                     "INS":"84",
                     "P1":"00",
                     "P2":"00",
                     "Lc":None,
                     "Data":None,
                     "Le":"08"})
        dict = DeviceManager().sendAPDU(apdu)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"]
            if statCode == StatCodeType.STAT_CODE_SUCCESS:
                return dict["msg"]

        return None

    def getSelectFileDict(self,pos):
        LogManager().addLog("Selecting File")
        apdu = APDU({"CLA": "00",
                     "INS": "A4",
                     "P1": "00",
                     "P2": "00",
                     "Lc": "02",
                     "Data": self.getFID(pos),
                     "Le": None})
        dict = DeviceManager().sendAPDU(apdu)
        return dict

    def getSelectPKIADFDict(self):
        mfDict = self.getSelectFileDict(FileLocationType.MF)
        if (mfDict != None) and ('statCode' in mfDict):
            statCode = mfDict["statCode"]
            if statCode == StatCodeType.STAT_CODE_SUCCESS:
                adfDict = self.getSelectFileDict(FileLocationType.ADF)
                return adfDict
        return None

    pass