from Data.Test import *
from Controller.Helper import *

class TEST_BINARY_READ(Test):

    def run(self):
        superResult = super().run()

        dict = Helper().getSelectFileDict(FileLocationType.MF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        LogManager().addLogStr("NAVIGATE TO MF",LogType.Info,self.getTestType())

        dict = Helper().getSelectFileDict(FileLocationType.ADF)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False

        LogManager().addLogStr("NAVIGATE TO ADF", LogType.Info, self.getTestType())

        dict = Helper().getSelectFileDict(FileLocationType.EFTokenInfo)
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False
            print(dict["msg"])

        LogManager().addLogStr("NAVIGATE TO EF TOKEN INFO", LogType.Info, self.getTestType())

        dict = Helper().getBinaryReadDict("00","00")
        if (dict != None) and ('statCode' in dict):
            statCode = dict["statCode"].statCode
            if statCode != StatCodeType.STAT_CODE_SUCCESS:
                return False
            print(dict["msg"])

        LogManager().addLogStr("READ MSG = " + str(dict["msg"]), LogType.Info, self.getTestType())

        return True

    @staticmethod
    def getInfo():
        return "测试二进制读"

    @staticmethod
    def getTestType():
        return TestType.TEST_BINARY_READ