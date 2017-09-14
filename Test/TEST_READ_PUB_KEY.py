from Data.Test import *
from Controller.Helper import *
from Controller.DeviceManager import *
from Data.StatCode import *

class TEST_READ_PUB_KEY(Test):

    def run(self):
        superResult = super().run()

        dict = Helper().getSelectFileDict(FileLocationType.MF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"]
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        dict = Helper().getSelectFileDict(FileLocationType.ADF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"]
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        dict = Helper().getPubKeyDict("00")
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode == StatCodeType.STAT_CODE_SUCCESS:
                return True

    @staticmethod
    def getInfo():
        return "测试读取公钥"

    @staticmethod
    def getTestType():
        return TestType.TEST_READ_PUB_KEY